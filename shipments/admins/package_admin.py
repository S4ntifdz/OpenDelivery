from django.contrib import admin
from unfold.admin import ModelAdmin

from shipments.models import PackageModel


@admin.register(PackageModel)
class PackageAdmin(ModelAdmin):
    list_display = ("uuid", "shipment", "weight", "volume", "description", "value")
    search_fields = ("description",)
    raw_id_fields = ("shipment",)
