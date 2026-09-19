from django.urls import path

from . import views

app_name = "skills"

urlpatterns = [
    path("assessment/", views.take_assessment, name="assessment"),
]