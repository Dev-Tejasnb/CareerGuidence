from django.contrib import admin

from .models import Skill, SkillAssessment, SkillRating


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "description")
    list_filter = ("category",)


class SkillRatingInline(admin.TabularInline):
    model = SkillRating
    extra = 0


@admin.register(SkillAssessment)
class SkillAssessmentAdmin(admin.ModelAdmin):
    list_display = ("user", "taken_at", "completed")
    list_filter = ("completed", "taken_at")
    inlines = [SkillRatingInline]