from uuid import UUID
import logging

from ninja import Router
from shipments.schemas import (
    ShipmentCreateIn, 
    ShipmentOut, 
    ShipmentQuoteIn, 
    ShipmentQuoteOut
)
from shipments.services.shipment_service import ShipmentService

logger = logging.getLogger(__name__)

router = Router()

@router.post("/", response={202: ShipmentOut})
def create_shipment(request, payload: ShipmentCreateIn):
    """Crea un envío delegando la comunicación externa asíncronamente a Celery. (Retorna 202 Inmediato)"""
    tenant = getattr(request, "tenant", None)
    logger.info(f"[Router] create_shipment - tenant={tenant}, payload={payload.dict()}")
    shipment = ShipmentService.create_shipment(payload, tenant=tenant)
    return 202, shipment

@router.post("/quotes", response={201: ShipmentQuoteOut})
def get_shipment_quote(request, payload: ShipmentQuoteIn):
    """Obtiene una cotización de un carrier y la persiste localmente."""
    tenant = getattr(request, "tenant", None)
    logger.info(
        f"[Router] get_shipment_quote - tenant={tenant}, "
        f"origin_lat={payload.origin_location.latitude}, origin_lng={payload.origin_location.longitude}, "
        f"dest_lat={payload.destination_location.latitude}, dest_lng={payload.destination_location.longitude}"
    )
    try:
        quote = ShipmentService.get_quote(payload, tenant=tenant)
        return 201, quote
    except Exception as e:
        logger.exception(f"[Router] get_shipment_quote FAILED: {e}")
        raise

@router.get("/{shipment_id}/tracking")
def get_shipment_tracking(request, shipment_id: UUID):
    """Consulta el estado del partner de envío."""
    try:
        tracking_info = ShipmentService.get_tracking(str(shipment_id))
        return tracking_info
    except ValueError as e:
        return router.create_response(request, {"error": str(e)}, status=404)

@router.post("/{shipment_id}/cancel")
def cancel_shipment(request, shipment_id: UUID):
    try:
        result = ShipmentService.cancel_shipment(str(shipment_id))
        return result
    except ValueError as e:
        return router.create_response(request, {"error": str(e)}, status=404)
