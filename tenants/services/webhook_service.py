from tenants.services.webhook_tasks import notify_tenant_webhook

class WebhookService:
    """
    Servicio para orquestar el envío de notificaciones a los comercios.
    """

    @staticmethod
    def notify_status_change(shipment):
        """
        Notifica al Tenant de un cambio en el estado de un envío.
        """
        tenant = shipment.tenant
        if not tenant or not tenant.webhook_url:
            return

        payload = {
            "event": "shipment.status_updated",
            "data": {
                "shipment_uuid": str(shipment.uuid),
                "reference_id": shipment.reference_id,
                "status": shipment.status,
                "tracking_url": shipment.tracking_url,
                "external_id": shipment.external_id,
            }
        }

        # Encolar tarea de Celery
        notify_tenant_webhook.delay(
            tenant.webhook_url,
            payload,
            tenant.webhook_api_key
        )

    @staticmethod
    def notify_tracking_event(event):
        """
        Notifica al Tenant sobre un nuevo evento de tracking recibido.
        """
        shipment = event.shipment
        tenant = shipment.tenant
        if not tenant or not tenant.webhook_url:
            return

        payload = {
            "event": "shipment.tracking_updated",
            "data": {
                "shipment_uuid": str(shipment.uuid),
                "reference_id": shipment.reference_id,
                "event_type": event.event_type,
                "notes": event.notes,
                "timestamp": event.created_at.isoformat(),
            }
        }

        # Encolar tarea de Celery
        notify_tenant_webhook.delay(
            tenant.webhook_url,
            payload,
            tenant.webhook_api_key
        )
