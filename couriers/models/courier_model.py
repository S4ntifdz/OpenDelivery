from django.db import models

from core.models import BaseModel
from couriers.enums import CourierStatus


class CourierModel(BaseModel):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=50)
    status = models.CharField(
        max_length=20,
        choices=CourierStatus.choices,
        default=CourierStatus.OFFLINE,
    )
    vehicle = models.OneToOneField(
        "couriers.VehicleModel",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="courier",
    )
    tenant = models.ForeignKey(
        "tenants.TenantModel",
        on_delete=models.CASCADE,
        related_name="couriers",
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "couriers_courier"
        verbose_name = "Courier"
        verbose_name_plural = "Couriers"

    def __str__(self):
        return f"{self.name} [{self.status}]"
