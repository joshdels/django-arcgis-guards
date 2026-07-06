from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    """The corporate customer paying for guard services."""

    name = models.CharField(max_length=255)
    ogranization = models.CharField(max_length=255, blank=True)
    billing_email = models.EmailField()
    invoice_cycle_days = models.IntegerField(
        default=30, help_text="Billing frequency in days"
    )
    next_billing_date = models.DateField()
    hourly_billing_rate = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Amount client pays per hour"
    )

    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Guard(models.Model):
    """The security guards employed by your agency."""

    guard_name = models.OneToOneField(User, on_delete=models.CASCADE)
    guard_email = models.EmailField()
    badge_number = models.CharField(max_length=50, unique=True)
    hourly_pay_rate = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Amount guard earns per hour"
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.badge_number})"


class GuardAssignment(models.Model):
    """Tracks which guards are deployed to which clients for a shift."""

    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="assignments"
    )
    guard = models.ForeignKey(
        Guard, on_delete=models.CASCADE, related_name="assignments"
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    is_invoiced = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Automatically compute total shift hours if end_time exists
        if self.start_time and self.end_time:
            delta = self.end_time - self.start_time
            self.hours_worked = decimal.Decimal(delta.total_seconds() / 3600.0)
        super().save(*args, **kwargs)


class Invoice(models.Model):
    """Financial statements generated per client billing cycle."""

    STATUS_CHOICES = [("PENDING", "Pending"), ("PAID", "Paid"), ("OVERDUE", "Overdue")]

    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="invoices"
    )
    issued_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="PENDING")

    def __str__(self):
        return f"INV-{self.id} for {self.client.name}"
