from django.db import models
from apps.client.models import Client
from apps.operation.models import Job


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
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="jobs")
    invoice_number = models.CharField(max_length=30, unique=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING
    )


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="items")
    description = models.TextField(blank=True)
    quantity = models.PositiveIntegerField()
    amount = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_length=10, max_digits=2)


class Payment(models.Model):
    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, related_name="payments"
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateField()
    method = models.CharField(max_length=255, blank=True)
    reference_no = models.CharField(max_length=255, blank=True)
