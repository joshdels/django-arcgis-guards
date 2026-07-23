from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property

from apps.client.models import Client


class ContractStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    PENDING = "pending", "Pending"
    APPROVED = "approved", "Approved"
    ONGOING = "ongoing", "Ongoing"
    FINISHED = "finished", "Finished"
    CANCELLED = "cancelled", "Cancelled"


class BillingCycle(models.TextChoices):
    WEEKLY = "weekly", "Weekly"
    BIWEEKLY = "biweekly", "Biweekly"
    MONTHLY = "monthly", "Monthly"
    QUARTERLY = "quarterly", "Quarterly"
    CUSTOM = "custom", "Custom"


class BillingType(models.TextChoices):
    HOURLY = "hourly", "Hourly"
    DAILY = "daily", "Daily"
    MONTHLY_FIXED = "monthly_fixed", "Monthly Fixed"
    CUSTOM = "custom", "Custom"


class PaymentTerms(models.TextChoices):
    DUE_ON_RECEIPT = "due_on_receipt", "Due on Receipt"
    NET_7 = "net_7", "Net 7 Days"
    NET_15 = "net_15", "Net 15 Days"
    NET_30 = "net_30", "Net 30 Days"
    CUSTOM = "custom", "Custom"


class Contract(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="contracts",
    )

    contract_number = models.CharField(
        max_length=50,
        unique=True,
        editable=False,
    )

    title = models.CharField(
        max_length=255,
    )

    description = models.TextField(
        blank=True,
    )

    location = models.CharField(
        max_length=255,
        blank=True,
    )

    number_of_guards = models.PositiveIntegerField(
        default=1,
        help_text="Required number of guards.",
    )

    billing_cycle = models.CharField(
        max_length=20,
        choices=BillingCycle.choices,
        default=BillingCycle.MONTHLY,
    )

    billing_type = models.CharField(
        max_length=20,
        choices=BillingType.choices,
        default=BillingType.MONTHLY_FIXED,
    )

    rate = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Rate according to the selected billing type.",
        null=True,
    )

    payment_terms = models.CharField(
        max_length=30,
        choices=PaymentTerms.choices,
        default=PaymentTerms.NET_30,
    )

    tax_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        help_text="Tax percentage applied to billings.",
    )

    start_date = models.DateField()

    end_date = models.DateField(
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    status = models.CharField(
        max_length=20,
        choices=ContractStatus.choices,
        default=ContractStatus.DRAFT,
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

    @cached_property
    def allocated_guard_count(self):
        return sum(deployment.required_guards for deployment in self.deployments.all())

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contract"
        verbose_name_plural = "Contracts"

        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["start_date"]),
            models.Index(fields=["end_date"]),
        ]

    def __str__(self):
        return f"{self.contract_number} - {self.client.name}"

    def save(self, *args, **kwargs):
        if not self.contract_number:
            year = timezone.now().year

            last = (
                Contract.objects.filter(contract_number__startswith=f"CON-{year}")
                .order_by("-id")
                .first()
            )

            number = int(last.contract_number.split("-")[-1]) + 1 if last else 1

            self.contract_number = f"CON-{year}-{number:04d}"

        super().save(*args, **kwargs)


class ContractDocument(models.Model):
    contract = models.ForeignKey(
        Contract,
        on_delete=models.CASCADE,
        related_name="documents",
    )

    title = models.CharField(
        max_length=255,
    )

    file = models.FileField(
        upload_to="contracts/documents/",
    )

    remarks = models.TextField(
        blank=True,
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["title"]
        verbose_name = "Contract Document"
        verbose_name_plural = "Contract Documents"

    def __str__(self):
        return self.title
