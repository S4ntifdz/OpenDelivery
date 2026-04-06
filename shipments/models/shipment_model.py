from django.db import models
from django.db.models import Q
from django.conf import settings

from core.models import BaseModel
from shipments.enums import ShipmentStatus, ProviderType


class ShipmentManager(models.Manager):
    def get_by_reference_or_external(self, search_id: str):
        """
        Busca un envío independientemente de si el cliente introduce
        el ID interno (uuid principal), de referencia rápida o del proveedor externo.
        """
        # Intentamos parsear uuid para evitar errores de db en bases strictly-typed como PostgreSQL
        search_filter = Q(reference_id=search_id) | Q(external_id=search_id)
        
        # Validar si tiene formato de UUID (36 chars con 4 guiones)
        if len(search_id) == 36 and search_id.count('-') == 4:
            search_filter |= Q(uuid=search_id)
            
        return self.filter(search_filter).first()


class ShipmentModel(BaseModel):
    objects = ShipmentManager()

    reference_id = models.CharField(max_length=100, unique=True)
    provider = models.CharField(
        max_length=20,
        choices=ProviderType.choices,
        default=ProviderType.INTERNAL,
    )
    status = models.CharField(
        max_length=20,
        choices=ShipmentStatus.choices,
        default=ShipmentStatus.CREATED,
    )
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    external_id = models.CharField(max_length=255, blank=True, default="")
    tracking_url = models.URLField(max_length=500, blank=True, default="")
    scheduled_at = models.DateTimeField(null=True, blank=True)

    origin_location = models.ForeignKey(
        "shipments.LocationModel",
        on_delete=models.PROTECT,
        related_name="shipments_as_origin",
    )
    destination_location = models.ForeignKey(
        "shipments.LocationModel",
        on_delete=models.PROTECT,
        related_name="shipments_as_destination",
    )
    courier = models.ForeignKey(
        "couriers.CourierModel",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="shipments",
    )
    tenant = models.ForeignKey(
        "tenants.TenantModel",
        on_delete=models.CASCADE,
        related_name="shipments",
        null=True,
    )

    class Meta:
        db_table = "shipments_shipment"
        verbose_name = "Shipment"
        verbose_name_plural = "Shipments"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        """Sobreescribir save para autogenerar la URL de tracking si no existe."""
        # Se verifica si tracking_url está vacía (usualmente al crear el objeto la primera vez o si falló)
        if not self.tracking_url:
            # En este punto auto-creamos el id para usarlo (garantizamos UUID si aún no lo tiene pre save)
            super().save(*args, **kwargs)
            self.tracking_url = f"{settings.BASE_URL.rstrip('/')}/?tracking_id={self.uuid}"
            # Volver a guardar el objeto para asentar la URL sin causar loop infinito (via update_fields si es posible, o normal)
            return super().save(update_fields=["tracking_url", "updated_at"])

        return super().save(*args, **kwargs)

    def __str__(self):
        return f"Shipment {self.reference_id} [{self.status}]"