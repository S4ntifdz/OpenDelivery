from django.contrib import admin
from unfold.admin import ModelAdmin

from shipments.models import ShipmentModel


@admin.register(ShipmentModel)
class ShipmentAdmin(ModelAdmin):
    list_display = ("uuid", "reference_id", "provider", "status", "price", "scheduled_at", "created_at")
    search_fields = ("reference_id", "external_id")
    list_filter = ("status", "provider")
    readonly_fields = ("uuid", "created_at", "updated_at")
    raw_id_fields = ("origin_location", "destination_location", "courier")
