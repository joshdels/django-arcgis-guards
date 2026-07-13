from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_ADMIN = "ADMIN"
    ROLE_STAFF = "STAFF"
    ROLE_CLIENT = "CLIENT"
    ROLE_GUARD = "GUARD"

    ROLE_CHOICES = [
        (ROLE_ADMIN, "Admin"),
        (ROLE_STAFF, "Staff"),
        (ROLE_CLIENT, "Client"),
        (ROLE_GUARD, "Guard"),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=ROLE_GUARD,
    )

    def __str__(self):
        return self.get_full_name() or self.username