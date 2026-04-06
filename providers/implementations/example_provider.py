from providers.interfaces.shipping_provider import ShippingProvider
import logging

logger = logging.getLogger(__name__)

class ExampleProvider(ShippingProvider):
    """
    Example implementation of a Shipping Provider.
    Use this as a template to integrate new external services.
    """

    def create_shipment(self, shipment) -> dict:
        """
        Simulates creating a shipment with an external provider.
        Implement your API call here.
        """
        logger.info(f"Creating shipment for {shipment.id} with ExampleProvider")
        return {
            "status": "success",
            "provider_id": "EXAMPLE-12345",
            "tracking_number": "TRACK-EXP-999"
        }

    def cancel_shipment(self, shipment_id: str) -> dict:
        """
        Simulates canceling a shipment.
        """
        logger.info(f"Canceling shipment {shipment_id} with ExampleProvider")
        return {"status": "cancelled"}

    def get_tracking(self, shipment_id: str) -> dict:
        """
        Simulates getting tracking info.
        """
        logger.info(f"Getting tracking for {shipment_id} with ExampleProvider")
        return {
            "status": "in_transit",
            "last_update": "Shipment picked up by courier"
        }

    def get_quote(self, origin, destination) -> dict:
        """
        Simulates getting a shipping quote.
        """
        logger.info(f"Getting quote from {origin} to {destination} with ExampleProvider")
        return {
            "price": 10.0,
            "currency": "USD",
            "estimated_delivery": "2024-04-10"
        }
