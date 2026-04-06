import json
import requests
from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task(bind=True, max_retries=5, autoretry_for=(requests.RequestException,), retry_backoff=True)
def notify_tenant_webhook(self, webhook_url, payload, api_key=None):
    """
    Envía una notificación al webhook del comercio (Tenant).
    Envía la API Key en el header X-API-Key si está configurada.
    """
    logger.info(f"Sending simple webhook notification to {webhook_url}")
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "LogisticsCore-Webhook/1.0"
    }

    if api_key:
        # Usamos el mismo estándar de header que pedimos nosotros
        headers["X-API-Key"] = api_key

    try:
        response = requests.post(
            webhook_url,
            json=payload,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        logger.info(f"Webhook delivered successfully to {webhook_url}")
    except requests.RequestException as e:
        logger.warning(f"Failed to deliver webhook to {webhook_url}. Retrying... Error: {e}")
        raise e
