from django.contrib import admin
from django.urls import path, include
from core.views import HomeRedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomeRedirectView.as_view(), name="home"),
    path("dds/", include("core.urls")),
    path("api/", include("core.api_urls")),
]
