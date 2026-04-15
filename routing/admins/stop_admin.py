from django.contrib import admin
from core.admin import MultiTenantModelAdmin
from routing.models import StopModel


@admin.register(StopModel)
class StopAdmin(MultiTenantModelAdmin):
    list_display = ("uuid", "route", "location", "sequence", "status", "arrived_at", "completed_at")
    list_filter = ("status",)
    raw_id_fields = ("route", "location")
