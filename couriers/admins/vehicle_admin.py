from django.contrib import admin
from core.admin import MultiTenantModelAdmin
from couriers.models import VehicleModel


@admin.register(VehicleModel)
class VehicleAdmin(MultiTenantModelAdmin):
    list_display = ("uuid", "type", "capacity_weight", "capacity_volume")
    search_fields = ("type",)
