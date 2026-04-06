from django.db import models

from core.models import BaseModel
from shipments.enums import ProviderType


class ShipmentQuoteModel(BaseModel):
    price = models.DecimalField(max_digits=12, decimal_places=2)
    provider = models.CharField(
        max_length=20,
        choices=ProviderType.choices,
    )
    expires_at = models.DateTimeField()

    origin_location = models.ForeignKey(
        "shipments.LocationModel",
        on_delete=models.CASCADE,
        related_name="quotes_as_origin",
    )
    destination_location = models.ForeignKey(
        "shipments.LocationModel",
        on_delete=models.CASCADE,
        related_name="quotes_as_destination",
    )

    class Meta:
        db_table = "shipments_shipment_quote"
        verbose_name = "Shipment Quote"
        verbose_name_plural = "Shipment Quotes"

    def __str__(self):
        return f"Quote {self.provider} - ${self.price}"
