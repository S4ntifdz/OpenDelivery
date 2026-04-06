from abc import ABC, abstractmethod


class ShippingProvider(ABC):
    """
    Strategy Interface para proveedores de envío.

    Define el contrato que toda estrategia de shipping debe implementar.
    Se usa junto con provider_factory.get_provider() para resolver
    la estrategia concreta en runtime según el ProviderType.

    Estrategias concretas:
        - InternalCourierProvider (flota propia)
        - ExampleProvider (plantilla para integraciones externas)
    """

    @abstractmethod
    def create_shipment(self, shipment) -> dict:
        """Crear un envío con el proveedor."""
        ...

    @abstractmethod
    def cancel_shipment(self, shipment_id: str) -> dict:
        """Cancelar un envío existente."""
        ...

    @abstractmethod
    def get_tracking(self, shipment_id: str) -> dict:
        """Obtener información de tracking de un envío."""
        ...

    @abstractmethod
    def get_quote(self, origin, destination) -> dict:
        """Obtener cotización para un origen y destino dados."""
        ...
