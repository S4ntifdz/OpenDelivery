from django.db import models


class TaskType(models.TextChoices):
    PICKUP = "PICKUP", "Pickup"
    DROPOFF = "DROPOFF", "Dropoff"
