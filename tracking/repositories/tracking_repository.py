from typing import Optional

from tracking.models import TrackingEventModel
from shipments.models import ShipmentModel

class TrackingRepository:
    """Repositorio para gestionar eventos de seguimiento."""

    @staticmethod
    def add_event(shipment: ShipmentModel, event_type: str, notes: str = "", location: str = "", source: str = "SYSTEM"):
        """Registra un nuevo evento histórico inmutable en la base de datos."""
        return TrackingEventModel.objects.create(
            shipment=shipment,
            event_type=event_type,
            notes=notes,
            location=location,
            source=source,
        )

    @staticmethod
    def get_history_by_shipment(shipment_uuid: str):
        """Devuelve el historial completo de un envío ordenado de más reciente a más antiguo."""
        # Se asume que el ORM ya tiene '-timestamp' en la clase Meta del modelo.
        return TrackingEventModel.objects.filter(shipment_id=shipment_uuid)
