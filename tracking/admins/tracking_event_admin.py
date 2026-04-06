from django.contrib import admin
from unfold.admin import ModelAdmin

from tracking.models import TrackingEventModel


@admin.register(TrackingEventModel)
class TrackingEventAdmin(ModelAdmin):
    list_display = ("uuid", "shipment", "event_type", "timestamp", "source")
    search_fields = ("notes", "source")
    list_filter = ("event_type", "source")
    raw_id_fields = ("shipment", "location")
    readonly_fields = ("uuid", "created_at", "updated_at")
