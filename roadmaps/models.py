from django.conf import settings
from django.db import models


class Roadmap(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="roadmaps",
    )
    career = models.ForeignKey(
        "careers.Career",
        on_delete=models.CASCADE,
        related_name="roadmaps",
    )
    readiness_score = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "career")

    def __str__(self):
        return f"{self.user}: {self.career}"

    @property
    def progress_percentage(self):
        total = self.steps.count()
        done = self.steps.filter(status=RoadmapStep.Status.COMPLETED).count()
        return round(done / total * 100) if total else 0


class RoadmapStep(models.Model):
    class Status(models.TextChoices):
        NOT_STARTED = "not_started", "Not Started"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"

    roadmap = models.ForeignKey(
        Roadmap,
        on_delete=models.CASCADE,
        related_name="steps",
    )
    skill = models.ForeignKey(
        "skills.Skill",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="roadmap_steps",
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NOT_STARTED,
    )

    STATUS_CHOICES = Status.choices

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.order}. {self.title}"