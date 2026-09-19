from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from roadmaps.models import Roadmap
from .models import Career
from .services import analyze_career, user_ratings


@login_required
def dashboard(request):
    ratings = user_ratings(request.user)
    careers = []
    for career in Career.objects.prefetch_related("career_skills"):
        careers.append((career, analyze_career(career, ratings)["score"]))
    careers.sort(key=lambda c: c[1], reverse=True)

    roadmaps = request.user.roadmaps.select_related("career")
    best = careers[0][1] if careers else 0
    has_assessment = request.user.assessments.filter(completed=True).exists()

    return render(request, "careers/dashboard.html", {
        "careers": careers,
        "roadmaps": roadmaps,
        "best_career": careers[0][0] if careers else None,
        "best_score": best,
        "has_assessment": has_assessment,
    })


@login_required
def career_list(request):
    ratings = user_ratings(request.user)
    careers = []
    for career in Career.objects.prefetch_related("career_skills"):
        analysis = analyze_career(career, ratings)
        careers.append({
            "career": career,
            "score": analysis["score"],
            "gap_count": len(analysis["gaps"]),
        })
    careers.sort(key=lambda c: c["score"], reverse=True)
    return render(request, "careers/list.html", {"careers": careers})


@login_required
def career_detail(request, pk):
    career = get_object_or_404(Career.objects.prefetch_related("career_skills"), pk=pk)
    ratings = user_ratings(request.user)
    analysis = analyze_career(career, ratings)
    roadmap = Roadmap.objects.filter(user=request.user, career=career).first()
    return render(request, "careers/detail.html", {
        "career": career,
        "analysis": analysis,
        "roadmap": roadmap,
    })