import json
from django.db.models import Count
from shipments.models import ShipmentModel
from shipments.enums import ShipmentStatus

def dashboard_context(request):
    """
    Context processor to provide dashboard data to the admin index.
    """
    if not request.path == "/admin/" and not request.path == "/admin":
        return {}
    
    if not request.user.is_authenticated or not request.user.is_staff:
        return {}
    
    # Filtering logic for multi-tenancy
    qs = ShipmentModel.objects.all()
    if not request.user.is_superuser:
        if hasattr(request.user, "profile") and request.user.profile.tenant:
            qs = qs.filter(tenant=request.user.profile.tenant)
        else:
            return {}

    # KPIs
    total = qs.count()
    delivered = qs.filter(status=ShipmentStatus.DELIVERED).count()
    in_transit = qs.filter(status=ShipmentStatus.IN_TRANSIT).count()
    failed = qs.filter(status=ShipmentStatus.FAILED).count()

    # Chart 1: Status Distribution
    status_counts = qs.values("status").annotate(count=Count("pk")).order_by("-count")
    status_data = {
        "labels": [s["status"] for s in status_counts],
        "datasets": [{
            "data": [s["count"] for s in status_counts],
            "backgroundColor": ["#6366f1", "#22c55e", "#3b82f6", "#ef4444", "#f59e0b", "#64748b"]
        }]
    }
    
    context = {
        "kpi_total": total,
        "kpi_delivered": delivered,
        "kpi_in_transit": in_transit,
        "kpi_failed": failed,
        "status_chart": json.dumps(status_data),
    }

    # Chart 2: Tenant Distribution (Superuser only)
    if request.user.is_superuser:
        tenant_counts = ShipmentModel.objects.values("tenant__name").annotate(count=Count("pk")).order_by("-count")
        tenant_data = {
            "labels": [s["tenant__name"] or "Unknown" for s in tenant_counts],
            "datasets": [{
                "data": [s["count"] for s in tenant_counts],
                "backgroundColor": "#6366f1"
            }]
        }
        context["tenant_chart"] = json.dumps(tenant_data)

    return context
