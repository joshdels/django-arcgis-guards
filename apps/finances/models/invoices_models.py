from decimal import Decimal
from django.utils import timezone
from django.db import models
from django.db.models import Sum
from django.core.exceptions import ValidationError

from apps.finances.models import Billing


class InvoiceStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    SENT = "sent", "Sent"
    PAID = "paid", "Paid"
    OVERDUE = "overdue", "Overdue"
    CANCELLED = "cancelled", "Cancelled"


class Invoice(models.Model):
    invoice_number = models.CharField(
        max_length=50,
        unique=True,
        editable=False,
    )

    billing = models.OneToOneField(
        Billing,
        on_delete=models.PROTECT,
        related_name="invoice",
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    issue_date = models.DateField(
        auto_now_add=True,
    )

    due_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=InvoiceStatus.choices,
        default=InvoiceStatus.DRAFT,
    )

    remarks = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    @property
    def amount_paid(self):
        return self.payments.filter(status="completed").aggregate(total=Sum("amount"))[
            "total"
        ] or Decimal("0.00")

    @property
    def balance_due(self):
        return self.total_amount - self.amount_paid

    def update_status(self):
        if self.amount_paid >= self.total_amount:
            self.status = InvoiceStatus.PAID
        else:
            self.status = InvoiceStatus.SENT

        self.save(update_fields=["status"])

    def clean(self):
        if self.due_date and self.issue_date and self.due_date < self.issue_date:
            raise ValidationError(
                {"due_date": "Due date cannot be before the issue date."}
            )

    def save(self, *args, **kwargs):
        if self.billing_id:
            self.total_amount = self.billing.total_amount

        self.full_clean()

        if not self.invoice_number:
            year = timezone.now().year

            last = (
                Invoice.objects.filter(invoice_number__startswith=f"INV-{year}")
                .order_by("-id")
                .first()
            )

            number = int(last.invoice_number.split("-")[-1]) + 1 if last else 1

            self.invoice_number = f"INV-{year}-{number:04d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.invoice_number} - {self.billing.contract.client.name}"
