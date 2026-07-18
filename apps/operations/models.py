from django.db import models

from django.core.exceptions import ValidationError

from apps.contract.models import Contract
from apps.guard.models import Guard


class Deployment(models.Model):
    contract = models.ForeignKey(
        Contract, on_delete=models.CASCADE, related_name="deployments"
    )

    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    required_guards = models.PositiveIntegerField(default=1)
    remarks = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.contract.contract_number} - {self.name}"


class AssignmentStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    ENDED = "ENDED", "Ended"
    CANCELLED = "CANCELLED", "Cancelled"


class Assignment(models.Model):
    deployment = models.ForeignKey(
        Deployment, on_delete=models.CASCADE, related_name="assignments"
    )

    guard = models.ForeignKey(
        Guard, on_delete=models.CASCADE, related_name="assignments"
    )

    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    status = models.CharField(
        max_length=20, choices=AssignmentStatus.choices, default=AssignmentStatus.ACTIVE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-start_date"]

    def clean(self):
        if self.end_date and self.end_date < self.start_date:
            raise ValidationError("End date cannot be before start date.")

    def __str__(self):
        return f"{self.guard} -> {self.deployment}"
