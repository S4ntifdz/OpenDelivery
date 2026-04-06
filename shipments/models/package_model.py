from django.db import models

from core.models import BaseModel


class PackageModel(BaseModel):
    shipment = models.ForeignKey(
        "shipments.ShipmentModel",
        on_delete=models.CASCADE,
        related_name="packages",
    )
    weight = models.FloatField(default=0, help_text="Weight in kg")
    volume = models.FloatField(default=0, help_text="Volume in m³")
    description = models.CharField(max_length=255, blank=True, default="")
    value = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        db_table = "shipments_package"
        verbose_name = "Package"
        verbose_name_plural = "Packages"

    def __str__(self):
        return f"Package ({self.weight}kg) - {self.description}"
