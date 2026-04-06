from django.contrib import admin
from unfold.admin import ModelAdmin

from couriers.models import CourierModel


@admin.register(CourierModel)
class CourierAdmin(ModelAdmin):
    list_display = ("uuid", "name", "phone", "status", "vehicle")
    search_fields = ("name", "phone")
    list_filter = ("status",)
    raw_id_fields = ("vehicle",)
