from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models


class Client(models.Model):
    """Company that hires security guards."""

    name = models.CharField(max_length=255)
    organization = models.CharField(max_length=255, blank=True)

    billing_email = models.EmailField()

    invoice_cycle_days = models.PositiveIntegerField(default=30)
    next_billing_date = models.DateField()

    hourly_billing_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Guard(models.Model):
    """Security guard employed by the agency."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="guard_profile",
    )

    badge_number = models.CharField(
        max_length=50,
    )

    hourly_pay_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    phone_number = models.CharField(
        max_length=30,
        blank=True,
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.badge_number})"


class GuardAssignment(models.Model):
    """
    Assigns a guard to a client.
    One assignment can have many attendance records.
    """

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
        return f"{self.guard} -> {self.client}"


class GuardAttendance(models.Model):
    """
    Daily login/logout of a guard.
    """

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


class Invoice(models.Model):
    STATUS_PENDING = "PENDING"
    STATUS_PAID = "PAID"
    STATUS_OVERDUE = "OVERDUE"

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
