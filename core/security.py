from django.conf import settings
from ninja.security import APIKeyHeader
from tenants.models import TenantModel

class ApiKeyAuth(APIKeyHeader):
    param_name = "X-API-Key"

    def authenticate(self, request, key):
        """
        Valida que el token ingresado coincida con un Tenant activo en la BD.
        """
        try:
            tenant = TenantModel.objects.get(api_key=key, is_active=True)
            request.tenant = tenant # Adherimos el tenant al request para usarlo en routers/services
            return tenant
        except TenantModel.DoesNotExist:
            return None
