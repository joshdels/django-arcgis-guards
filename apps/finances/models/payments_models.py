from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from decimal import Decimal
from django.db.models import Sum

from apps.finances.models import Invoice


class PaymentMethod(models.TextChoices):
    CASH = "cash", "Cash"
    BANK_TRANSFER = "bank_transfer", "Bank Transfer"
    CHECK = "check", "Check"
    ONLINE = "online", "Online Payment"
    OTHER = "other", "Other"


class PaymentStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    COMPLETED = "completed", "Completed"
    FAILED = "failed", "Failed"
    REFUNDED = "refunded", "Refunded"


class Payment(models.Model):
    payment_number = models.CharField(
        max_length=50,
        unique=True,
        editable=False,
    )

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.PROTECT,
        related_name="payments",
    )

    payment_date = models.DateField()

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
    )

    reference_number = models.CharField(
        max_length=100,
        blank=True,
        help_text="Bank transaction, OR number, check number, etc.",
        unique=True,
    )

    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
    )

    remarks = models.TextField(
        blank=True,
    )

    proof_of_payment = models.FileField(
        upload_to="payments/proofs/",
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-payment_date", "-created_at"]

        indexes = [
            models.Index(fields=["payment_date"]),
            models.Index(fields=["status"]),
        ]

    def clean(self):
        if self.amount <= Decimal("0.00"):
            raise ValidationError(
                {"amount": "Payment amount must be greater than zero."}
            )

        if self.payment_method != PaymentMethod.CASH and not self.reference_number:
            raise ValidationError(
                {
                    "reference_number": "Reference number is required for non-cash payments."
                }
            )

        paid = self.invoice.payments.filter(status=PaymentStatus.COMPLETED).exclude(
            pk=self.pk
        ).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")

        if paid + self.amount > self.invoice.total_amount:
            raise ValidationError(
                {"amount": "Payment exceeds the remaining invoice balance."}
            )

    def save(self, *args, **kwargs):
        self.full_clean()

        if not self.payment_number:
            year = timezone.now().year

            last = (
                Payment.objects.filter(payment_number__startswith=f"PAY-{year}")
                .order_by("-id")
                .first()
            )

            number = int(last.payment_number.split("-")[-1]) + 1 if last else 1

            self.payment_number = f"PAY-{year}-{number:04d}"

        super().save(*args, **kwargs)

        self.invoice.update_status()

    def __str__(self):
        return self.payment_number
