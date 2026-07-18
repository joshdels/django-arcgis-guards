from django.db import models

from apps.contract.models import Contract
from apps.guard.models import Guard


# Create your models here.
class Deployment(models.Model):
    contract = models.ForeignKey(
        Contract, on_delete=models.CASCADE, related_name="deployments"
    )

    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    required_guards = models.PositiveIntegerField(default=1)
    remarks = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.contract.contract_number} - {self.name}"


class Assignment(models.Model):
    deployment = models.ForeignKey(
        Deployment, on_delete=models.CASCADE, related_name="assignments"
    )

    guard = models.ForeignKey(
        Guard, on_delete=models.CASCADE, related_name="assignments"
    )

    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-start_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["deployment", "guard"],
                name="unique_guard_deployment",
            )
        ]

    def __str__(self):
        return f"{self.guard} -> {self.deployment}"
