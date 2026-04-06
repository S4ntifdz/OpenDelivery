from django.contrib import admin
from unfold.admin import ModelAdmin

from routing.models import TaskModel


@admin.register(TaskModel)
class TaskAdmin(ModelAdmin):
    list_display = ("uuid", "stop", "type", "completed_at")
    list_filter = ("type",)
    raw_id_fields = ("stop",)
