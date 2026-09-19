from django.urls import path

from . import views

app_name = "careers"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("", views.career_list, name="list"),
    path("<int:pk>/", views.career_detail, name="detail"),
]