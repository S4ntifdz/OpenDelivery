from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.decorators import display
from django.utils.translation import gettext_lazy as _

from core.admin import MultiTenantModelAdmin
from shipments.models import ShipmentModel
from shipments.enums import ShipmentStatus


@admin.register(ShipmentModel)
class ShipmentAdmin(MultiTenantModelAdmin):
    list_display = (
        "reference_id",
        "tenant",
        "provider",
        "status_label",
        "price",
        "scheduled_at",
        "created_at",
    )
    search_fields = ("reference_id", "external_id")
    list_filter = ("status", "provider", "tenant")
    readonly_fields = ("uuid", "created_at", "updated_at")
    raw_id_fields = ("origin_location", "destination_location", "courier", "tenant")

    @display(
        description=_("Status"),
        label={
            ShipmentStatus.DELIVERED: "success",
            ShipmentStatus.FAILED: "danger",
            ShipmentStatus.CANCELLED: "danger",
            ShipmentStatus.IN_TRANSIT: "info",
            ShipmentStatus.PICKED_UP: "info",
            ShipmentStatus.ASSIGNED: "warning",
            ShipmentStatus.CREATED: "primary",
        },
    )
    def status_label(self, obj):
        return obj.status
