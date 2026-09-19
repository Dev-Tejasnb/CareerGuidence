from django.urls import path

from . import views

app_name = "roadmaps"

urlpatterns = [
    path("career/<int:career_pk>/create/", views.create_roadmap, name="create"),
    path("<int:roadmap_id>/", views.detail, name="detail"),
    path("<int:roadmap_id>/step/<int:step_id>/", views.update_step, name="update_step"),
]