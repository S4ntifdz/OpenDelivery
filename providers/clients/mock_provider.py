import uuid
import logging
from typing import Dict, Any

from providers.interfaces.shipping_provider import ShippingProvider

logger = logging.getLogger(__name__)

class MockProvider(ShippingProvider):
    """
    Proveedor de pruebas (Mock) para ambiente de Sandbox.
    Simula la integración con un Courier sin realizar llamadas HTTP.
    """

    def create_shipment(self, shipment_data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"[MOCK] Creating shipment: {shipment_data.get('reference_id')}")
        return {
            "external_id": f"MOCK-{uuid.uuid4().hex[:8].upper()}",
            "status": "CREATED",
            "tracking_url": "http://localhost:8000/mock-tracking",
            "raw_response": {"message": "Simulated success"}
        }

    def get_tracking(self, external_id: str) -> Dict[str, Any]:
        logger.info(f"[MOCK] Getting tracking for: {external_id}")
        return {
            "status": "IN_TRANSIT",
            "history": [
                {"status": "CREATED", "timestamp": "2023-12-01T10:00:00Z"},
                {"status": "IN_TRANSIT", "timestamp": "2023-12-01T12:00:00Z"}
            ]
        }

    def cancel_shipment(self, external_id: str) -> bool:
        logger.info(f"[MOCK] Cancelling shipment: {external_id}")
        return True

    def get_quote(self, shipment_data: Dict[str, Any]) -> Dict[str, Any]:
        """ Simula una cotización con un precio fijo. """
        logger.info(f"[MOCK] Quoting shipment for {shipment_data.get('origin_location', {}).get('address')} -> {shipment_data.get('destination_location', {}).get('address')}")
        return {
            "price": 750.00,
            "distance": 5.4,
            "currency": "$",
            "expires_at": "2023-12-01T20:00:00Z" # Mock static expiry
        }
