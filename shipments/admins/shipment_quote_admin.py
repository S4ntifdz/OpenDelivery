from django.contrib import admin
from unfold.admin import ModelAdmin

from shipments.models import ShipmentQuoteModel


@admin.register(ShipmentQuoteModel)
class ShipmentQuoteAdmin(ModelAdmin):
    list_display = ("uuid", "provider", "price", "expires_at", "created_at")
    list_filter = ("provider",)
    raw_id_fields = ("origin_location", "destination_location")
