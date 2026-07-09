from django.conf import settings
from django.db import models


class Client(models.Model):
    """Company that hires security guards."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="client_profile",
        null=True,
        blank=True,
    )

    name = models.CharField(max_length=255)
    organization = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)

    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)

    invoice_cycle_days = models.PositiveIntegerField(default=30)
    next_billing_date = models.DateField()

    hourly_billing_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def status(self):
        latest_invoice = self.invoices.last()
        return latest_invoice.status if latest_invoice else "Unknown"

    def __str__(self):
        return self.name


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
        Client,
        on_delete=models.CASCADE,
        related_name="invoices",
    )

    billing_start = models.DateField()
    billing_end = models.DateField()

    issued_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()

    total_hours = models.DecimalField(
        max_digits=8,
        decimal_places=2,
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice #{self.pk} - {self.client.name}"
