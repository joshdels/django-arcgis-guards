from django.db import models
from apps.client.models import Client
from apps.operation.models import Job


# Create your models here.
class Invoice(models.Model):
    STATUS_PENDING = "pending"
    STATUS_PAID = "paid"
    STATUS_OVERDUE = "overdue"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_PAID, "Paid"),
        (STATUS_OVERDUE, "Overdue"),
    ]

    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="invoices"
    )
    jobs = models.ForeignKey(Job, on_delete=models.CASCAD, related_name="jobs")
    invoice_number = models
    issue_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField
    subtotal = models.DecimalField(max_length=10, max_digits=2)
    tax = models.DecimalField(max_length=10, max_digits=2)
    total = models.DecimalField(max_length=10, max_digits=2)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING
    )


class InvoiceItem:
    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, related_name="invoice"
    )
    description = models.TextField(blank=True)
    quantity = models.IntegerField(max_length=10)
    unit_price = models.DecimalField(max_length=10, max_digits=2)
    amount = models.IntegerField(max_length=10)


class Payment(models.Model):
    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, related_name="invoice"
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateField()
    method = models.CharField(max_length=255, blank=True)
    reference_no = models.CharField(max_length=255, blank=True)
