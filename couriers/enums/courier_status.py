from django.db import models


class CourierStatus(models.TextChoices):
    AVAILABLE = "AVAILABLE", "Available"
    BUSY = "BUSY", "Busy"
    OFFLINE = "OFFLINE", "Offline"
