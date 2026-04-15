from django.contrib import admin
from core.admin import MultiTenantModelAdmin
from tracking.models import TrackingEventModel


@admin.register(TrackingEventModel)
class TrackingEventAdmin(MultiTenantModelAdmin):
    list_display = ("uuid", "shipment", "event_type", "timestamp", "source")
    search_fields = ("notes", "source")
    list_filter = ("event_type", "source")
    raw_id_fields = ("shipment", "location")
    readonly_fields = ("uuid", "created_at", "updated_at")
