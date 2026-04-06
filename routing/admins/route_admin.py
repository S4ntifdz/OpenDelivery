from django.contrib import admin
from unfold.admin import ModelAdmin

from routing.models import RouteModel


@admin.register(RouteModel)
class RouteAdmin(ModelAdmin):
    list_display = ("uuid", "shipment", "courier", "status", "estimated_distance", "estimated_duration", "created_at")
    list_filter = ("status",)
    raw_id_fields = ("shipment", "courier")
    readonly_fields = ("uuid", "created_at", "updated_at")
