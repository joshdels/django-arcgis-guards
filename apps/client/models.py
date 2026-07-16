from django.conf import settings
from django.db import models
from django.utils import timezone


class Client(models.Model):
    """Company that hires security guards."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="client_profile",
        null=True,
        blank=True,
    )
    
    client_id = models.CharField(max_length=255, blank=True, null=True)

    name = models.CharField(max_length=255)
    organization = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)

    contact_person = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)

    invoice_cycle_days = models.PositiveIntegerField(default=30)
    next_billing_date = models.DateField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        if self.organization:
            return f"{self.name} - {self.organization}"
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.client_id:
            year = timezone.now().year

            last = (
                Client.objects.filter(client_id__startswith=f"C-{year}")
                .order_by("-id")
                .first()
            )

            if last:
                number = int(last.client_id.split("-")[-1]) + 1
            else:
                number = 1

            self.client_id = f"C-{year}-{number:04d}"

        super().save(*args, **kwargs)
