from decimal import Decimal

from django.conf import settings
from django.db import models

from apps.client.models import Client


class Guard(models.Model):
    """Security guard employed by the agency."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="guard_profile",
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

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.badge_number})"


class GuardAssignment(models.Model):
    """Assigns a guard to a client."""

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="assignments",
    )

    guard = models.ForeignKey(
        Guard,
        on_delete=models.CASCADE,
        related_name="assignments",
    )

    assigned_from = models.DateField()

    assigned_until = models.DateField(
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.guard} → {self.client}"


class GuardAttendance(models.Model):
    """Daily attendance of a guard."""

    assignment = models.ForeignKey(
        GuardAssignment,
        on_delete=models.CASCADE,
        related_name="attendance",
    )

    time_in = models.DateTimeField()

    time_out = models.DateTimeField(
        null=True,
        blank=True,
    )

    hours_worked = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
    )

    is_invoiced = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-time_in"]

    def save(self, *args, **kwargs):
        if self.time_in and self.time_out:
            seconds = (self.time_out - self.time_in).total_seconds()
            self.hours_worked = Decimal(seconds / 3600).quantize(Decimal("0.01"))

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.assignment.guard} - {self.time_in.date()}"
