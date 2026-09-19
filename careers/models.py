from django.db import models


class Career(models.Model):
    title = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    salary_range = models.CharField(max_length=100, blank=True)
    demand_level = models.CharField(max_length=50, blank=True)
    skills = models.ManyToManyField(
        "skills.Skill",
        through="CareerSkill",
        related_name="careers",
    )

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title

    def skill_links(self):
        return self.career_skills.select_related("skill")


class CareerSkill(models.Model):
    """Links a career to a skill with a relative importance weight (1-5)."""
    career = models.ForeignKey(
        Career,
        on_delete=models.CASCADE,
        related_name="career_skills",
    )
    skill = models.ForeignKey(
        "skills.Skill",
        on_delete=models.CASCADE,
        related_name="career_links",
    )
    importance = models.PositiveSmallIntegerField(default=3)

    class Meta:
        unique_together = ("career", "skill")

    def __str__(self):
        return f"{self.career} / {self.skill} (importance {self.importance})"