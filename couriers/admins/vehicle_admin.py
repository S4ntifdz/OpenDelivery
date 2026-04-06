from django.contrib import admin
from unfold.admin import ModelAdmin

from couriers.models import VehicleModel


@admin.register(VehicleModel)
class VehicleAdmin(ModelAdmin):
    list_display = ("uuid", "type", "capacity_weight", "capacity_volume")
    search_fields = ("type",)
