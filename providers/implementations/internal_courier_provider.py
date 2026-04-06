from providers.interfaces import ShippingProvider


class InternalCourierProvider(ShippingProvider):
    """
    Estrategia concreta: Flota interna de couriers.

    Implementa ShippingProvider para envíos manejados
    con couriers propios de la empresa.
    """

    def create_shipment(self, shipment) -> dict:
        return self.assign_courier(shipment)

    def cancel_shipment(self, shipment_id: str) -> dict:
        raise NotImplementedError("TODO: implement internal cancel")

    def get_tracking(self, shipment_id: str) -> dict:
        raise NotImplementedError("TODO: implement internal tracking")

    def get_quote(self, origin, destination) -> dict:
        raise NotImplementedError("TODO: implement internal quote")

    # --- Métodos específicos de flota interna ---

    def assign_courier(self, shipment) -> dict:
        """Asignar un courier disponible al envío."""
        raise NotImplementedError("TODO: implement courier assignment logic")
