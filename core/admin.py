from django.contrib import admin
from unfold.admin import ModelAdmin

class MultiTenantModelAdmin(ModelAdmin):
    """
    Base ModelAdmin for multi-tenant data isolation.
    If the user is not a superuser, it filters results by their tenant.
    """
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        
        if hasattr(request.user, "profile") and request.user.profile.tenant:
            tenant = request.user.profile.tenant
            # Direct tenant field check
            if hasattr(self.model, "tenant"):
                return qs.filter(tenant=tenant)
            
            # Special case for TenantModel itself
            if self.model.__name__ == "TenantModel":
                return qs.filter(uuid=tenant.uuid)
                
            # Handle relations (e.g., TrackingEvent -> Shipment -> Tenant)
            # This is a bit more complex, but we can try common paths
            if hasattr(self.model, "shipment"):
                return qs.filter(shipment__tenant=tenant)
            
            if hasattr(self.model, "route") and hasattr(self.model.route.field.related_model, "shipment"):
                return qs.filter(route__shipment__tenant=tenant)

        return qs.none()

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser and not change:
            if hasattr(request.user, "profile") and request.user.profile.tenant:
                if hasattr(obj, "tenant"):
                    obj.tenant = request.user.profile.tenant
        super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if hasattr(request.user, "profile") and request.user.profile.tenant:
                tenant = request.user.profile.tenant
                related_model = db_field.remote_field.model
                
                if hasattr(related_model, "tenant"):
                    kwargs["queryset"] = related_model.objects.filter(tenant=tenant)
                elif hasattr(related_model, "shipment"):
                    kwargs["queryset"] = related_model.objects.filter(shipment__tenant=tenant)
                    
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
