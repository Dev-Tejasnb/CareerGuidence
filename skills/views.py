from collections import OrderedDict

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import Skill, SkillAssessment, SkillRating


@login_required
def take_assessment(request):
    """Show all skills for self-rating, or the latest in-progress ratings."""
    latest = request.user.assessments.filter(completed=False).first()
    if latest is None:
        latest = SkillAssessment.objects.create(user=request.user)

    existing = {str(r.skill_id): str(r.self_rating) for r in latest.ratings.all()}
    skills = Skill.objects.all()

    if request.method == "POST":
        for skill in skills:
            value = request.POST.get(f"skill_{skill.id}")
            if value and value.isdigit():
                rating = int(value)
                SkillRating.objects.update_or_create(
                    assessment=latest,
                    skill=skill,
                    defaults={"self_rating": rating},
                )
        latest.completed = True
        latest.save()
        return redirect("careers:list")

    return render(request, "skills/assessment.html", {
        "grouped": _group_skills(skills),
        "existing": existing,
    })


def _group_skills(skills):
    grouped = OrderedDict()
    for skill in skills:
        grouped.setdefault(skill.category, []).append(skill)
    return grouped