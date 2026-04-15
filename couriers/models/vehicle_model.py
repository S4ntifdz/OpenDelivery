from django.db import models

from core.models import BaseModel


class VehicleModel(BaseModel):
    type = models.CharField(max_length=50)
    capacity_weight = models.FloatField(default=0, help_text="Max weight in kg")
    capacity_volume = models.FloatField(default=0, help_text="Max volume in m³")
    tenant = models.ForeignKey(
        "tenants.TenantModel",
        on_delete=models.CASCADE,
        related_name="vehicles",
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "couriers_vehicle"
        verbose_name = "Vehicle"
        verbose_name_plural = "Vehicles"

    def __str__(self):
        return f"{self.type} ({self.capacity_weight}kg)"
