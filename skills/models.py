from django.db import models


class SkillCategory(models.TextChoices):
    TECHNICAL = "technical", "Technical"
    SOFT = "soft", "Soft Skill"


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(
        max_length=20,
        choices=SkillCategory.choices,
        default=SkillCategory.TECHNICAL,
    )
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class SkillAssessment(models.Model):
    """A single completed/attempted self-assessment for a user."""
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="assessments",
    )
    taken_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    class Meta:
        ordering = ["-taken_at"]

    def __str__(self):
        return f"{self.user} assessment @ {self.taken_at:%Y-%m-%d %H:%M}"


class SkillRating(models.Model):
    """Self-reported proficiency (1-5) for a skill within an assessment."""
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    assessment = models.ForeignKey(
        SkillAssessment,
        on_delete=models.CASCADE,
        related_name="ratings",
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name="ratings",
    )
    self_rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)

    class Meta:
        unique_together = ("assessment", "skill")

    def __str__(self):
        return f"{self.skill}: {self.self_rating}/5"