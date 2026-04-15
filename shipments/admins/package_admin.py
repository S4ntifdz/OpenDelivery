from django.contrib import admin
from core.admin import MultiTenantModelAdmin
from shipments.models import PackageModel


@admin.register(PackageModel)
class PackageAdmin(MultiTenantModelAdmin):
    list_display = ("uuid", "shipment", "weight", "volume", "description", "value")
    search_fields = ("description",)
    raw_id_fields = ("shipment",)
