from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.contract.models import Contract


class Guard(models.Model):
    """Security guard employed by the agency."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="guard_profile",
        null=True,
        blank=True,
    )

    first_name = models.CharField(max_length=100, blank=True, null=True)
    middle_name = models.CharField(max_length=100, default="", blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)

    badge_number = models.CharField(max_length=50)

    email = models.EmailField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(
        max_length=20,
        blank=True,
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.badge_number} - {self.first_name} {self.last_name} "

    def save(self, *args, **kwargs):
        if not self.badge_number:
            year = timezone.now().year

            last = (
                Guard.objects.filter(badge_number__startswith=f"G-{year}")
                .order_by("-id")
                .first()
            )

            if last:
                number = int(last.badge_number.split("-")[-1]) + 1
            else:
                number = 1

            self.badge_number = f"G-{year}-{number:04d}"

        super().save(*args, **kwargs)


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
