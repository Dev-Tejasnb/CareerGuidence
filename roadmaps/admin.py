from django.contrib import admin

from .models import Roadmap, RoadmapStep


class RoadmapStepInline(admin.TabularInline):
    model = RoadmapStep
    extra = 0


@admin.register(Roadmap)
class RoadmapAdmin(admin.ModelAdmin):
    list_display = ("user", "career", "readiness_score", "created_at")
    inlines = [RoadmapStepInline]