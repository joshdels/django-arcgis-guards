from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.client.models import Client
from apps.guard.models import Guard

User = get_user_model()


class Command(BaseCommand):
    help = "Seed demo clients and guards."

    def handle(self, *args, **kwargs):
        self.stdout.write("Cleaning existing demo data...")

        Guard.objects.all().delete()
        Client.objects.all().delete()
        User.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("✓ Existing demo data removed."))

        # ------------------------------------------------------------------
        # USERS
        # ------------------------------------------------------------------
        self.stdout.write("Creating users...")

        User.objects.create_superuser(
            username="admin",
            password="admin123",
            first_name="System",
            last_name="Administrator",
            email="admin@example.com",
            role=User.ROLE_ADMIN,
        )

        User.objects.create_user(
            username="staff",
            password="password123",
            first_name="Jane",
            last_name="Staff",
            email="staff@example.com",
            role=User.ROLE_STAFF,
        )

        # Guards
        juan = User.objects.create_user(
            username="juan",
            password="password123",
            first_name="Juan",
            last_name="Dela Cruz",
            email="juan@example.com",
            role=User.ROLE_GUARD,
        )

        pedro = User.objects.create_user(
            username="pedro",
            password="password123",
            first_name="Pedro",
            last_name="Santos",
            email="pedro@example.com",
            role=User.ROLE_GUARD,
        )

        maria = User.objects.create_user(
            username="maria",
            password="password123",
            first_name="Maria",
            last_name="Reyes",
            email="maria@example.com",
            role=User.ROLE_GUARD,
        )

        # Clients
        client1_user = User.objects.create_user(
            username="abc",
            password="password123",
            first_name="ABC",
            last_name="Manager",
            email="billing@abc.com",
            role=User.ROLE_CLIENT,
        )

        client2_user = User.objects.create_user(
            username="ceburoyale",
            password="password123",
            first_name="Cebu",
            last_name="Royale",
            email="finance@ceburoyale.com",
            role=User.ROLE_CLIENT,
        )

        client3_user = User.objects.create_user(
            username="southmall",
            password="password123",
            first_name="South",
            last_name="Mall",
            email="finance@southmall.com",
            role=User.ROLE_CLIENT,
        )

        # ------------------------------------------------------------------
        # CLIENTS
        # ------------------------------------------------------------------
        self.stdout.write("Creating clients...")

        Client.objects.create(
            user=client1_user,
            name="ABC Manufacturing",
            organization="ABC Manufacturing Inc.",
            location="Dumaguete City",
            contact_person="Juan Dela Cruz",
            email="billing@abc.com",
            phone="09171234567",
            invoice_cycle_days=30,
            next_billing_date=date(2026, 8, 1),
            hourly_billing_rate=Decimal("180.00"),
        )

        Client.objects.create(
            user=client2_user,
            name="Cebu Royale",
            organization="Aboitiz",
            location="Cebu City",
            contact_person="Maria Santos",
            email="finance@ceburoyale.com",
            phone="09172345678",
            invoice_cycle_days=30,
            next_billing_date=date(2026, 8, 1),
            hourly_billing_rate=Decimal("180.00"),
        )

        Client.objects.create(
            user=client3_user,
            name="South Mall",
            organization="South Mall Corporation",
            location="Bacolod City",
            contact_person="Pedro Reyes",
            email="finance@southmall.com",
            phone="09179876543",
            invoice_cycle_days=30,
            next_billing_date=date(2026, 8, 5),
            hourly_billing_rate=Decimal("200.00"),
        )

        # ------------------------------------------------------------------
        # GUARDS
        # ------------------------------------------------------------------
        self.stdout.write("Creating guards...")

        Guard.objects.create(
            user=juan,
            badge_number="G001",
            hourly_pay_rate=Decimal("90.00"),
            address="Dumaguete City",
            phone_number="09170000001",
        )

        Guard.objects.create(
            user=pedro,
            badge_number="G002",
            hourly_pay_rate=Decimal("95.00"),
            address="Cebu City",
            phone_number="09170000002",
        )

        Guard.objects.create(
            user=maria,
            badge_number="G003",
            hourly_pay_rate=Decimal("100.00"),
            address="Bacolod City",
            phone_number="09170000003",
        )

        self.stdout.write(self.style.SUCCESS("✓ Demo data seeded successfully."))
