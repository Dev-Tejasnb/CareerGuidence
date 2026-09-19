from django.contrib import admin

from .models import Career, CareerSkill


class CareerSkillInline(admin.TabularInline):
    model = CareerSkill
    extra = 0


@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ("title", "salary_range", "demand_level")
    search_fields = ("title", "description")
    inlines = [CareerSkillInline]