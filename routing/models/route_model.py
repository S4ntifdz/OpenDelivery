from django.db import models

from core.models import BaseModel
from routing.enums import RouteStatus


class RouteModel(BaseModel):
    shipment = models.ForeignKey(
        "shipments.ShipmentModel",
        on_delete=models.CASCADE,
        related_name="routes",
    )
    courier = models.ForeignKey(
        "couriers.CourierModel",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="routes",
    )
    status = models.CharField(
        max_length=20,
        choices=RouteStatus.choices,
        default=RouteStatus.PENDING,
    )
    estimated_distance = models.FloatField(
        null=True,
        blank=True,
        help_text="Estimated distance in km",
    )
    estimated_duration = models.FloatField(
        null=True,
        blank=True,
        help_text="Estimated duration in minutes",
    )

    class Meta:
        db_table = "routing_route"
        verbose_name = "Route"
        verbose_name_plural = "Routes"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Route {self.uuid} [{self.status}]"
