from django.db import models
from apps.client.models import Client
from apps.guard.models import Guard


class Job(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, relate_name="invoices")
    title = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10)


class Assignment(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, relate_name="jobs")
    guard = models.ForeignKey(Guard)
    shift = models.CharField()
    daily_rate = models.DecimalField(max_length=10, max_digits=2)
    start_date = models.DateField()
    end_date = models.DateField()
