from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe
from unfold.admin import ModelAdmin, TabularInline
from core.admin import MultiTenantModelAdmin
from .models import TenantModel, Profile
from .widgets.api_key_button_widget import RegenerableInputWidget

class TenantAdminForm(forms.ModelForm):
    class Meta:
        model = TenantModel
        fields = "__all__"
        widgets = {
            "api_key": RegenerableInputWidget(prefix="key_"),
            "webhook_api_key": RegenerableInputWidget(prefix="wh_key_", button_text="✨ Generate API Key"),
        }

class ProfileInline(TabularInline):
    model = Profile
    extra = 1

@admin.register(TenantModel)
class TenantAdmin(MultiTenantModelAdmin):
    form = TenantAdminForm
    list_display = ("name", "default_provider", "is_active", "webhook_url", "created_at")
    search_fields = ("name", "api_key", "webhook_url")
    list_filter = ("is_active", "default_provider")
    inlines = [ProfileInline]
    
    fieldsets = (
        (None, {
            "fields": ("name", "default_provider", "is_active")
        }),
        ("Inbound API Security", {
            "fields": ("api_key",),
            "description": "Credentials the merchant uses to access our API."
        }),
        ("Outbound API Security (Webhooks)", {
            "fields": ("webhook_url", "webhook_api_key"),
            "description": "Configuration used to notify the merchant's API (e.g. Comandaya)."
        }),
    )

    class Media:
        js = ("js/api_key_gen.js",)

@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display = ("user", "tenant", "created_at")
    list_filter = ("tenant",)
    search_fields = ("user__username", "user__email", "tenant__name")
