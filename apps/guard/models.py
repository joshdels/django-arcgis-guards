from django.conf import settings
from django.db import models

from apps.operation.models import Contract


class Guard(models.Model):
    """Security guard employed by the agency."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="guard_profile",
        null=True,
        blank=True,
    )

    badge_number = models.CharField(max_length=50)

    hourly_pay_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    address = models.CharField(max_length=255, blank=True)

    phone_number = models.CharField(
        max_length=20,
        blank=True,
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)


class GuardAssignment(models.Model):
    contract = models.ForeignKey(
        Contract,
        related_name="assignments",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    guard = models.ForeignKey(
        Guard,
        related_name="assignment",
        on_delete=models.CASCADE,
    )

    assigned_at = models.DateField()
    relieved_at = models.DateField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
