"""Root URL configuration for the Career Readiness Navigator."""

from django.contrib import admin
from django.urls import include, path

from accounts.views import home

urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("skills/", include("skills.urls")),
    path("careers/", include("careers.urls")),
    path("roadmaps/", include("roadmaps.urls")),
]