from django.contrib import admin
from core.admin import MultiTenantModelAdmin
from shipments.models import LocationModel


@admin.register(LocationModel)
class LocationAdmin(MultiTenantModelAdmin):
    list_display = ("uuid", "address", "city", "postal_code", "contact_name", "contact_phone")
    search_fields = ("address", "city", "contact_name", "contact_phone")
    list_filter = ("city",)
