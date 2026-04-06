from django.contrib import admin
from unfold.admin import ModelAdmin

from tracking.models import TrackingEventModel


@admin.register(TrackingEventModel)
class TrackingEventAdmin(ModelAdmin):
    list_display = ("uuid", "shipment", "event_type", "timestamp", "source")
    search_fields = ("shipment__reference_id", "shipment__external_id", "notes", "source")
    list_filter = ("event_type", "source")
    readonly_fields = ("uuid", "timestamp", "created_at", "updated_at")
