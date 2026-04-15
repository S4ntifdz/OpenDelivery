from django.contrib import admin
from core.admin import MultiTenantModelAdmin
from routing.models import TaskModel


@admin.register(TaskModel)
class TaskAdmin(MultiTenantModelAdmin):
    list_display = ("uuid", "stop", "type", "completed_at")
    list_filter = ("type",)
    raw_id_fields = ("stop",)
