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

    contact_person = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)

    invoice_cycle_days = models.PositiveIntegerField(default=30)
    next_billing_date = models.DateField(null=True, blank=True)

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
