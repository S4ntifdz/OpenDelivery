from django.db import models
from django.utils import timezone

from core.models import BaseModel
from tracking.enums import TrackingEventType


class TrackingEventModel(BaseModel):
    shipment = models.ForeignKey(
        "shipments.ShipmentModel",
        on_delete=models.CASCADE,
        related_name="tracking_events",
    )
    event_type = models.CharField(
        max_length=20,
        choices=TrackingEventType.choices,
    )
    timestamp = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True, default="")
    location = models.ForeignKey(
        "shipments.LocationModel",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tracking_events",
    )
    source = models.CharField(
        max_length=50,
        blank=True,
        default="",
        help_text="Origin of the event, e.g. 'external_webhook', 'internal'",
    )

    class Meta:
        db_table = "tracking_tracking_event"
        verbose_name = "Tracking Event"
        verbose_name_plural = "Tracking Events"
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.event_type} @ {self.timestamp}"
