from datetime import date, datetime
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from agency.models import (
    Client,
    Guard,
    GuardAssignment,
    GuardAttendance,
    Invoice,
)

User = get_user_model()


class Command(BaseCommand):
    help = "Seed the database with demo data."

    def handle(self, *args, **kwargs):
        self.stdout.write("Cleaning existing demo data...")

        GuardAttendance.objects.all().delete()
        Invoice.objects.all().delete()
        GuardAssignment.objects.all().delete()
        Guard.objects.all().delete()
        Client.objects.all().delete()
        User.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("✓ Existing demo data removed."))

        # ------------------------------------------------------------------
        # USERS
        # ------------------------------------------------------------------
        self.stdout.write("Creating users...")

        admin = User.objects.create_superuser(
            username="admin",
            password="admin123",
            first_name="System",
            last_name="Administrator",
            email="admin@example.com",
            role=User.ROLE_ADMIN,
        )

        staff = User.objects.create_user(
            username="staff",
            password="password123",
            first_name="Jane",
            last_name="Staff",
            email="staff@example.com",
            role=User.ROLE_STAFF,
        )

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

        client1_user = User.objects.create_user(
            username="abc",
            password="password123",
            first_name="ABC",
            last_name="Manager",
            email="billing@abc.com",
            role=User.ROLE_CLIENT,
        )

        client2_user = User.objects.create_user(
            username="southmall",
            password="password123",
            first_name="South",
            last_name="Mall",
            email="finance@southmall.com",
            role=User.ROLE_CLIENT,
        )

        client3_user = User.objects.create_user(
            username="northmail",
            password="password123",
            first_name="North",
            last_name="Logistics",
            email="logistics@northmail.com",
            role=User.ROLE_CLIENT,
        )

        # ------------------------------------------------------------------
        # CLIENTS
        # ------------------------------------------------------------------
        self.stdout.write("Creating clients...")

        abc = Client.objects.create(
            user=client1_user,
            name="ABC Manufacturing",
            organization="ABC Manufacturing Inc.",
            location="Dumaguete City",
            email="billing@abc.com",
            phone="09171234567",
            invoice_cycle_days=30,
            next_billing_date=date(2026, 8, 1),
            hourly_billing_rate=Decimal("180.00"),
        )

        north = Client.objects.create(
            user=client2_user,
            name="Cebu Royale",
            organization="Aboitez",
            location="Cebu City",
            email="billing@abc.com",
            phone="09171234567",
            invoice_cycle_days=30,
            next_billing_date=date(2026, 8, 1),
            hourly_billing_rate=Decimal("180.00"),
        )

        south = Client.objects.create(
            user=client3_user,
            name="South Mall",
            organization="South Mall Corporation",
            location="Bacolod City",
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

        g1 = Guard.objects.create(
            user=juan,
            badge_number="G001",
            hourly_pay_rate=Decimal("90.00"),
            phone_number="09170000001",
        )

        g2 = Guard.objects.create(
            user=pedro,
            badge_number="G002",
            hourly_pay_rate=Decimal("95.00"),
            phone_number="09170000002",
        )

        g3 = Guard.objects.create(
            user=maria,
            badge_number="G003",
            hourly_pay_rate=Decimal("100.00"),
            phone_number="09170000003",
        )

        # ------------------------------------------------------------------
        # ASSIGNMENTS
        # ------------------------------------------------------------------
        self.stdout.write("Creating assignments...")

        a1 = GuardAssignment.objects.create(
            client=abc,
            guard=g1,
            assigned_from=date(2026, 7, 1),
        )

        a2 = GuardAssignment.objects.create(
            client=north,
            guard=g2,
            assigned_from=date(2026, 7, 1),
        )

        a3 = GuardAssignment.objects.create(
            client=south,
            guard=g3,
            assigned_from=date(2026, 7, 5),
        )

        # ------------------------------------------------------------------
        # ATTENDANCE
        # ------------------------------------------------------------------
        self.stdout.write("Creating attendance records...")

        GuardAttendance.objects.create(
            assignment=a1,
            time_in=timezone.make_aware(datetime(2026, 7, 6, 8, 0)),
            time_out=timezone.make_aware(datetime(2026, 7, 6, 17, 0)),
        )

        GuardAttendance.objects.create(
            assignment=a1,
            time_in=timezone.make_aware(datetime(2026, 7, 7, 8, 0)),
            time_out=timezone.make_aware(datetime(2026, 7, 7, 17, 0)),
        )

        GuardAttendance.objects.create(
            assignment=a2,
            time_in=timezone.make_aware(datetime(2026, 7, 6, 8, 0)),
            time_out=timezone.make_aware(datetime(2026, 7, 6, 16, 0)),
        )

        GuardAttendance.objects.create(
            assignment=a2,
            time_in=timezone.make_aware(datetime(2026, 7, 7, 8, 0)),
            time_out=timezone.make_aware(datetime(2026, 7, 7, 16, 0)),
        )

        GuardAttendance.objects.create(
            assignment=a3,
            time_in=timezone.make_aware(datetime(2026, 7, 6, 7, 0)),
            time_out=timezone.make_aware(datetime(2026, 7, 6, 15, 0)),
        )

        GuardAttendance.objects.create(
            assignment=a3,
            time_in=timezone.make_aware(datetime(2026, 7, 7, 7, 0)),
            time_out=timezone.make_aware(datetime(2026, 7, 7, 15, 0)),
        )

        # ------------------------------------------------------------------
        # INVOICES
        # ------------------------------------------------------------------
        self.stdout.write("Creating invoices...")

        Invoice.objects.create(
            client=abc,
            billing_start=date(2026, 7, 1),
            billing_end=date(2026, 7, 31),
            due_date=date(2026, 8, 15),
            total_hours=Decimal("320.00"),
            total_amount=Decimal("57600.00"),
            status=Invoice.STATUS_PENDING,
        )

        Invoice.objects.create(
            client=north,
            billing_start=date(2026, 6, 1),
            billing_end=date(2026, 6, 30),
            due_date=date(2026, 7, 15),
            total_hours=Decimal("310.00"),
            total_amount=Decimal("55800.00"),
            status=Invoice.STATUS_PENDING,
        )

        Invoice.objects.create(
            client=south,
            billing_start=date(2026, 7, 1),
            billing_end=date(2026, 7, 31),
            due_date=date(2026, 8, 15),
            total_hours=Decimal("160.00"),
            total_amount=Decimal("32000.00"),
            status=Invoice.STATUS_OVERDUE,
        )

        self.stdout.write(self.style.SUCCESS("✓ Database seeded successfully."))