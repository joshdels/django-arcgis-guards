from django.db import models
from apps.client.models import Client
from apps.operation.models import Job


class Invoice(models.Model):
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="invoices"
    )
    job = models.ForeignKey(
        Job, on_delete=models.CASCADE, related_name="invoices", null=True, blank=True
    )
    invoice_number = models.CharField(max_length=100, unique=True)
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_paid = models.BooleanField(default=False)
