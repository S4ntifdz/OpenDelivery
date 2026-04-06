from django.contrib import admin
from django.urls import path, include

from LogisticsCore.api.v1 import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", api.urls),
    path("", include("web.urls", namespace="web")),  # Frontend Web App en ROOT
]

