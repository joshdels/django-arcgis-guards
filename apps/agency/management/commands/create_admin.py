from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Create the initial admin user."

    def handle(self, *args, **options):
        username = "admin"
        email = "admin@example.com"
        password = "admin123"

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING("Admin user already exists.")
            )
            return

        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )

        user.role = User.ROLE_ADMIN
        user.save(update_fields=["role"])

        self.stdout.write(
            self.style.SUCCESS("Superuser created successfully.")
        )