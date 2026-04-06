from typing import List
from uuid import UUID

from ninja import Router

from tracking.schemas import TrackingEventIn, TrackingEventOut
from tracking.services.tracking_service import TrackingService

router = Router()

@router.post("/events", response={201: TrackingEventOut})
def register_tracking_event(request, payload: TrackingEventIn):
    """
    Registra un evento de seguimiento inmutable para un envío.
    Ideal para ser consumido por Webhooks de partners o apps de couriers propios.
    """
    try:
        event = TrackingService.register_event(payload)
        return 201, event
    except ValueError as e:
        return router.create_response(request, {"error": str(e)}, status=404)

@router.get("/shipments/{shipment_uuid}/events", response=List[TrackingEventOut])
def get_shipment_history(request, shipment_uuid: UUID):
    """
    Lista todos los eventos de seguimiento de un envío, 
    ordenados del más reciente al más antiguo.
    """
    try:
        history = TrackingService.get_shipment_history(str(shipment_uuid))
        return list(history)
    except ValueError as e:
        return router.create_response(request, {"error": str(e)}, status=404)
