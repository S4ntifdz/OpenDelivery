from shipments.repositories.shipment_repository import ShipmentRepository
from shipments.models import LocationModel
from tracking.repositories.tracking_repository import TrackingRepository
from tracking.models import TrackingEventModel
from tracking.schemas import TrackingEventIn
from tenants.services.webhook_service import WebhookService


class TrackingService:
    """
    Servicio principal de Dominio para Tracking.
    Gestiona el agregado manual de eventos y la obtención del historial completo.
    """

    @staticmethod
    def register_event(payload: TrackingEventIn) -> TrackingEventModel:
        """
        Registra un evento originado manualmente o a través de un Webhook.
        Aísla la validación del shipment y opcionalmente location.
        """
        # 1. Validar que el shipment exista en BD.
        # (Usamos el repository de Shipments para evitar acoplamiento de modelos)
        shipment = ShipmentRepository.get_by_uuid(str(payload.shipment_uuid))
        if not shipment:
            raise ValueError(f"Shipment {payload.shipment_uuid} not found")

        # 2. Manejo opcional de locación asociada al evento
        location_obj = None
        if payload.location_uuid:
            # En sistemas puros esto debería ir al LocationRepository, pero simplificamos
            location_obj = LocationModel.objects.filter(id=payload.location_uuid).first()

        # 3. Guardar Evento en BDD local de forma inmutable a través de TrackingRepository.
        event = TrackingRepository.add_event(
            shipment=shipment,
            event_type=payload.event_type,
            notes=payload.notes,
            location=location_obj,
            source=payload.source,
        )

        # 4. Notificar al Tenant vía Webhook (Async)
        WebhookService.notify_tracking_event(event)

        return event

    @staticmethod
    def get_shipment_history(shipment_uuid: str):
        """
        Obtiene el timeline local asíncrono.
        A diferencia de ShipmentService.get_tracking() que hace web-scraping/API poll a internet,
        este recoge de BD lo que ya se grabó previamente (vía webhooks o logs periódicos).
        """
        # Validación de existencia del envío
        shipment = ShipmentRepository.get_by_uuid(shipment_uuid)
        if not shipment:
            raise ValueError(f"Shipment {shipment_uuid} not found")
            
        history = TrackingRepository.get_history_by_shipment(shipment_uuid)
        return history
