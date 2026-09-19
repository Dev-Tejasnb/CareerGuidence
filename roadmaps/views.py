from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from careers.models import Career
from careers.services import analyze_career, user_ratings
from .models import Roadmap, RoadmapStep


@login_required
def create_roadmap(request, career_pk):
    career = get_object_or_404(Career, pk=career_pk)
    ratings = user_ratings(request.user)
    analysis = analyze_career(career, ratings)

    roadmap, created = Roadmap.objects.get_or_create(
        user=request.user,
        career=career,
        defaults={"readiness_score": analysis["score"]},
    )

    if created:
        _build_steps(roadmap, analysis["gaps"])
    return redirect("roadmaps:detail", roadmap_id=roadmap.id)


def _build_steps(roadmap, gaps):
    for idx, gap in enumerate(gaps, start=1):
        RoadmapStep.objects.create(
            roadmap=roadmap,
            skill=gap["skill"],
            order=idx,
            title=f"Develop {gap['skill'].name}",
            description=(
                f"Build {gap['skill'].name} from {gap['current']}/5 "
                f"to {gap['target']}/5. "
                f"{gap['skill'].description or 'See recommended learning resources.'}"
            ),
        )
    if not gaps:
        RoadmapStep.objects.create(
            roadmap=roadmap,
            order=1,
            title="Stay sharp and up to date",
            description="You're already strong in all core skills. Keep practicing "
                        "and consider advanced or adjacent topics.",
        )


@login_required
def detail(request, roadmap_id):
    roadmap = get_object_or_404(
        Roadmap.objects.prefetch_related("steps", "career"),
        id=roadmap_id,
        user=request.user,
    )
    return render(request, "roadmaps/detail.html", {"roadmap": roadmap})


@login_required
def update_step(request, roadmap_id, step_id):
    roadmap = get_object_or_404(Roadmap, id=roadmap_id, user=request.user)
    step = get_object_or_404(roadmap.steps, id=step_id)
    status = request.POST.get("status")
    if status in RoadmapStep.Status.values:
        step.status = status
        step.save()
    return redirect("roadmaps:detail", roadmap_id=roadmap.id)