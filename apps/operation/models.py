from django.db import models
from django.utils import timezone

from apps.client.models import Client


class ContractStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    ONGOING = "ongoing", "Ongoing"
    FINISHED = "finished", "Finished"
    CANCELLED = "cancelled", "Cancelled"


class Contract(models.Model):
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="contracts"
    )
    contract_number = models.CharField(max_length=50, unique=True, editable=False)

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255)

    number_of_guards = models.PositiveIntegerField(
        default=1,
        help_text="Number of guards required for this contract.",
    )

    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    status = models.CharField(
        max_length=20, choices=ContractStatus.choices, default=ContractStatus.PENDING
    )

    remarks = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contract"
        verbose_name_plural = "Contracts"

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

            if last:
                number = int(last.contract_number.split("-")[-1]) + 1
            else:
                number = 1

            self.contract_number = f"CON-{year}={number:004d}"

        super().save(*args, **kwargs)
