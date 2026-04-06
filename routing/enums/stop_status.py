from django.db import models


class StopStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    ARRIVED = "ARRIVED", "Arrived"
    COMPLETED = "COMPLETED", "Completed"
    SKIPPED = "SKIPPED", "Skipped"
