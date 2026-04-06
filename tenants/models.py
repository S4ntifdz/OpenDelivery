import secrets
from django.db import models
from core.models import BaseModel
from shipments.enums import ProviderType

class TenantModel(BaseModel):
    name = models.CharField(max_length=100, unique=True, help_text="Nombre del Comercio (ej: Bar de Lalo)")
    api_key = models.CharField(max_length=255, unique=True, db_index=True)
    default_provider = models.CharField(
        max_length=20,
        choices=ProviderType.choices,
        default=ProviderType.TEST,
        help_text="Estrategia de delivery por defecto para este comercio"
    )
    is_active = models.BooleanField(default=True)
    webhook_url = models.URLField(max_length=500, blank=True, null=True, help_text="URL donde el comercio recibirá actualizaciones de estado")
    webhook_api_key = models.CharField(max_length=255, blank=True, null=True, help_text="API Key que se enviará en el header X-API-Key al notificar al comercio")

    class Meta:
        db_table = "tenants_tenant"
        verbose_name = "Tenant"
        verbose_name_plural = "Tenants"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.api_key:
            self.api_key = f"key_{secrets.token_urlsafe(32)}"
        super().save(*args, **kwargs)
