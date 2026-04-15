import secrets
from django.db import models
from core.models import BaseModel
from shipments.enums import ProviderType

class TenantModel(BaseModel):
    name = models.CharField(max_length=100, unique=True, help_text="Merchant name (e.g. Oxxo)")
    api_key = models.CharField(max_length=255, unique=True, db_index=True)
    default_provider = models.CharField(
        max_length=20,
        choices=ProviderType.choices,
        default=ProviderType.TEST,
        help_text="Default delivery strategy for this merchant"
    )
    is_active = models.BooleanField(default=True)
    webhook_url = models.URLField(max_length=500, blank=True, null=True, help_text="URL where the merchant will receive status updates")
    webhook_api_key = models.CharField(max_length=255, blank=True, null=True, help_text="API Key sent in X-API-Key header when notifying the merchant")

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
from django.conf import settings
class Profile(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    tenant = models.ForeignKey(
        TenantModel,
        on_delete=models.CASCADE,
        related_name="profiles",
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "tenants_profile"
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return f"{self.user.username} - {self.tenant.name if self.tenant else 'Global'}"
