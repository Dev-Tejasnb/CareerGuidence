"""Business logic for skill gap analysis and readiness scoring.

A skill is considered a "gap" when the user's self-rated proficiency
falls below the target proficiency required for a career.
"""

TARGET_PROFICIENCY = 4


def user_ratings(user):
    """Return {skill_id: self_rating} from the user's most recent assessment."""
    assessment = user.assessments.filter(completed=True).first()
    if assessment is None:
        return {}
    return {
        r.skill_id: r.self_rating
        for r in assessment.ratings.select_related("skill")
    }


def analyze_career(career, ratings):
    """Compute skill gaps and readiness for a career given a ratings map.

    Returns a dict with:
        - score: int 0-100 weighted readiness score
        - gaps: list of {skill, current, target, importance}
        - strengths: list of {skill, rating}
    """
    links = career.career_skills.select_related("skill")

    total_weight = 0
    weighted_achieved = 0
    gaps = []
    strengths = []

    for link in links:
        skill = link.skill
        current = ratings.get(skill.id, 0)
        total_weight += link.importance
        ratio = min(current / TARGET_PROFICIENCY, 1.0)
        weighted_achieved += ratio * link.importance

        entry = {
            "skill": skill,
            "current": current,
            "target": TARGET_PROFICIENCY,
            "importance": link.importance,
        }
        if current < TARGET_PROFICIENCY:
            gaps.append(entry)
        else:
            strengths.append(entry)

    score = round(weighted_achieved / total_weight * 100) if total_weight else 0
    gaps.sort(key=lambda g: g["importance"], reverse=True)

    return {"score": score, "gaps": gaps, "strengths": strengths}