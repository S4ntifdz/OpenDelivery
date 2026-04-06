from django.db import models

from core.models import BaseModel
from routing.enums import StopStatus


class StopModel(BaseModel):
    route = models.ForeignKey(
        "routing.RouteModel",
        on_delete=models.CASCADE,
        related_name="stops",
    )
    location = models.ForeignKey(
        "shipments.LocationModel",
        on_delete=models.PROTECT,
        related_name="stops",
    )
    status = models.CharField(
        max_length=20,
        choices=StopStatus.choices,
        default=StopStatus.PENDING,
    )
    sequence = models.PositiveIntegerField(
        default=0,
        help_text="Order of the stop in the route",
    )
    arrived_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "routing_stop"
        verbose_name = "Stop"
        verbose_name_plural = "Stops"
        ordering = ["sequence"]

    def __str__(self):
        return f"Stop #{self.sequence} [{self.status}]"
