from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

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

    pdf = models.FileField(
        upload_to="invoices/",
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    @property
    def total_amount(self):
        return self.billing.total_amount

    class Meta:
        ordering = ["-issue_date"]
        indexes = [
            models.Index(fields=["status"]),
        ]

        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"

    def clean(self):
        if self.due_date and self.issue_date and self.due_date < self.issue_date:
            raise ValidationError(
                {"due_date": "Due date cannot be before the issue date."}
            )

    def save(self, *args, **kwargs):
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
