from django.db import models


class ProviderType(models.TextChoices):
    EXAMPLE = "EXAMPLE", "Example Provider"
    INTERNAL = "INTERNAL", "Internal"
    TEST = "TEST", "Test / Mock"
