from django.urls import path
from web.views import tracking_timeline_view

app_name = "web"

urlpatterns = [
    path("", tracking_timeline_view, name="tracking_timeline"),
]
