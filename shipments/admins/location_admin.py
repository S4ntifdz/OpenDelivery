from django.contrib import admin
from unfold.admin import ModelAdmin

from shipments.models import LocationModel


@admin.register(LocationModel)
class LocationAdmin(ModelAdmin):
    list_display = ("uuid", "address", "city", "postal_code", "contact_name", "contact_phone")
    search_fields = ("address", "city", "contact_name", "contact_phone")
    list_filter = ("city",)
