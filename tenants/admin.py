from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe
from unfold.admin import ModelAdmin
from .models import TenantModel
from .widgets.api_key_button_widget import RegenerableInputWidget

class TenantAdminForm(forms.ModelForm):
    class Meta:
        model = TenantModel
        fields = "__all__"
        widgets = {
            "api_key": RegenerableInputWidget(prefix="key_"),
            "webhook_api_key": RegenerableInputWidget(prefix="wh_key_", button_text="✨ Generar API Key"),
        }

@admin.register(TenantModel)
class TenantAdmin(ModelAdmin):
    form = TenantAdminForm
    list_display = ("name", "default_provider", "is_active", "webhook_url", "created_at")
    search_fields = ("name", "api_key", "webhook_url")
    list_filter = ("is_active", "default_provider")
    
    fieldsets = (
        (None, {
            "fields": ("name", "default_provider", "is_active")
        }),
        ("Seguridad & API ENTRANTE", {
            "fields": ("api_key",),
            "description": "Credenciales que el comercio usa para pegarle a nuestra API."
        }),
        ("Seguridad & API SALIENTE (Webhooks)", {
            "fields": ("webhook_url", "webhook_api_key"),
            "description": "Configuración para que nosotros le peguemos a la API del comercio (ej: Comandaya)."
        }),
    )

    class Media:
        js = ("js/api_key_gen.js",)
