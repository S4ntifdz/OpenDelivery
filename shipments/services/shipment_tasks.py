from celery import shared_task
from celery.utils.log import get_task_logger

from shipments.repositories.shipment_repository import ShipmentRepository
from shipments.enums import ShipmentStatus
from providers.factories.provider_factory import get_provider
from providers.exceptions import ProviderServerException

logger = get_task_logger(__name__)

@shared_task(bind=True, max_retries=3, autoretry_for=(ProviderServerException,), retry_backoff=True)
def process_shipment_creation(self, shipment_uuid: str, payload_data: dict):
    """
    Tarea asincrónica para dar de alta el envío en el Provider (ej: Ejemplo).
    Atrapa errores de servidor (502, 503 HTTP) y autos-reintenta hasta 3 veces.
    """
    logger.info(f"Processing shipment creation for {shipment_uuid}")
    
    shipment = ShipmentRepository.get_by_uuid(shipment_uuid)
    if not shipment:
        logger.error(f"Shipment {shipment_uuid} not found during async processing")
        return
        
    try:
        provider = get_provider(shipment.provider)
        # Llamada de red HTTP (Lenta)
        response_data = provider.create_shipment(payload_data)
        
        # Todo salio bien, actualizar Shipment a ASSIGNED (o IN_TRANSIT)
        ShipmentRepository.update_provider_data(
            shipment_uuid=shipment_uuid,
            external_id=response_data.get("external_id", ""),
            tracking_url=response_data.get("tracking_url", ""),
            new_status=ShipmentStatus.ASSIGNED,
        )
        logger.info(f"Shipment {shipment_uuid} successfully assigned to provider.")
        
    except Exception as e:
        # Falla fatal (ej. 400 Validation Error) o se acabaron los retries
        logger.exception(f"Fatal error requesting provider for shipment {shipment_uuid}: {e}")
        ShipmentRepository.update_status(shipment_uuid, ShipmentStatus.FAILED)
        raise e
