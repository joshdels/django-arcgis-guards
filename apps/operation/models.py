from django.db import models
from apps.client.models import Client
from apps.guard.models import Guard


class Job(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="jobs")
    title = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10)


class Assignment(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="assignments")
    guard = models.ForeignKey(
        Guard, on_delete=models.CASCADE, related_name="assignments"
    )
    shift = models.CharField(max_length=50, blank=True)
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)

    start_date = models.DateField()
    end_date = models.DateField()
