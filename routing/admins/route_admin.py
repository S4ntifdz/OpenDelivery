from django.contrib import admin
from core.admin import MultiTenantModelAdmin
from routing.models import RouteModel


@admin.register(RouteModel)
class RouteAdmin(MultiTenantModelAdmin):
    list_display = ("uuid", "shipment", "courier", "status", "estimated_distance", "estimated_duration", "created_at")
    list_filter = ("status",)
    raw_id_fields = ("shipment", "courier")
    readonly_fields = ("uuid", "created_at", "updated_at")
