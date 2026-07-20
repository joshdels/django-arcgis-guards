from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError

from apps.contract.models import Contract


class BillingStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    FINALIZED = "finalized", "Finalized"
    CANCELLED = "cancelled", "Cancelled"


class Billing(models.Model):
    billing_number = models.CharField(
        max_length=50,
        unique=True,
        editable=False,
    )

    contract = models.ForeignKey(
        Contract,
        on_delete=models.PROTECT,
        related_name="billings",
    )

    billing_period_start = models.DateField()
    billing_period_end = models.DateField()

    billing_date = models.DateField(
        help_text="Date this billing was generated.",
    )
    due_date = models.DateField()

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    tax = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    status = models.CharField(
        max_length=20,
        choices=BillingStatus.choices,
        default=BillingStatus.DRAFT,
    )

    is_manual = models.BooleanField(
        default=False,
        help_text="Whether this billing was manually created.",
    )

    remarks = models.TextField(blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_billings",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-billing_period_start", "-created_at"]

    def save(self, *args, **kwargs):
        self.full_clean()

        if not self.billing_number:
            year = timezone.now().year

            last = (
                Billing.objects.filter(billing_number__startswith=f"BILL-{year}")
                .order_by("-id")
                .first()
            )

            number = int(last.billing_number.split("-")[-1]) + 1 if last else 1

            self.billing_number = f"BILL-{year}-{number:04d}"

        super().save(*args, **kwargs)

    def clean(self):
        if self.billing_period_end < self.billing_period_start:
            raise ValidationError(
                {
                    "billing_period_end": "Billing period end cannot be before the start date."
                }
            )

        if self.due_date < self.billing_date:
            raise ValidationError(
                {"due_date": "Due date cannot be before the billing date."}
            )

    def __str__(self):
        return f"{self.billing_number} - {self.contract.client.name}"
