from providers.interfaces import ShippingProvider
from providers.implementations.example_provider import ExampleProvider
from providers.implementations.internal_courier_provider import InternalCourierProvider
from providers.clients.mock_provider import MockProvider
from shipments.enums.provider_type import ProviderType


def get_provider(provider_type: str) -> ShippingProvider:
    """
    Factory + Strategy Resolver.

    Resuelve la estrategia de shipping correcta según el ProviderType.
    Devuelve siempre la interfaz ShippingProvider, manteniendo
    el dominio desacoplado de las implementaciones concretas.

    Uso:
        provider = get_provider(shipment.provider)
        provider.create_shipment(shipment)
    """
    strategies: dict[str, type[ShippingProvider]] = {
        ProviderType.EXAMPLE: ExampleProvider,
        ProviderType.INTERNAL: InternalCourierProvider,
        ProviderType.TEST: MockProvider,
    }

    strategy_class = strategies.get(provider_type)
    if strategy_class is None:
        raise ValueError(f"Unknown provider type: {provider_type}")

    return strategy_class()
