from datetime import date, datetime
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from agency.models import (
    Client,
    Guard,
    GuardAssignment,
    GuardAttendance,
    Invoice,
)


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

        self.stdout.write("Creating users...")

        juan = User.objects.create_user(
            username="juan",
            password="password123",
            first_name="Juan",
            last_name="Dela Cruz",
        )

        pedro = User.objects.create_user(
            username="pedro",
            password="password123",
            first_name="Pedro",
            last_name="Santos",
        )

        maria = User.objects.create_user(
            username="maria",
            password="password123",
            first_name="Maria",
            last_name="Reyes",
        )

        self.stdout.write("Creating clients...")

        abc = Client.objects.create(
            name="ABC Manufacturing",
            organization="ABC Manufacturing Inc.",
            billing_email="billing@abc.com",
            invoice_cycle_days=30,
            next_billing_date=date(2026, 8, 1),
            hourly_billing_rate=Decimal("180.00"),
        )

        south = Client.objects.create(
            name="South Mall",
            organization="South Mall Corporation",
            billing_email="finance@southmall.com",
            invoice_cycle_days=30,
            next_billing_date=date(2026, 8, 5),
            hourly_billing_rate=Decimal("200.00"),
        )

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

        self.stdout.write("Creating assignments...")

        a1 = GuardAssignment.objects.create(
            client=abc,
            guard=g1,
            assigned_from=date(2026, 7, 1),
        )

        a2 = GuardAssignment.objects.create(
            client=abc,
            guard=g2,
            assigned_from=date(2026, 7, 1),
        )

        a3 = GuardAssignment.objects.create(
            client=south,
            guard=g3,
            assigned_from=date(2026, 7, 5),
        )

        self.stdout.write("Creating attendance...")

        GuardAttendance.objects.create(
            assignment=a1,
            time_in=timezone.make_aware(datetime(2026, 7, 6, 8, 0)),
            time_out=timezone.make_aware(datetime(2026, 7, 6, 17, 0)),
        )

        GuardAttendance.objects.create(
            assignment=a2,
            time_in=timezone.make_aware(datetime(2026, 7, 6, 8, 0)),
            time_out=timezone.make_aware(datetime(2026, 7, 6, 16, 0)),
        )

        GuardAttendance.objects.create(
            assignment=a3,
            time_in=timezone.make_aware(datetime(2026, 7, 6, 7, 0)),
            time_out=timezone.make_aware(datetime(2026, 7, 6, 15, 0)),
        )

        self.stdout.write("Creating invoices...")

        Invoice.objects.create(
            client=abc,
            billing_start=date(2026, 7, 1),
            billing_end=date(2026, 7, 31),
            due_date=date(2026, 8, 15),
            total_hours=Decimal("320.00"),
            total_amount=Decimal("57600.00"),
        )

        Invoice.objects.create(
            client=south,
            billing_start=date(2026, 7, 1),
            billing_end=date(2026, 7, 31),
            due_date=date(2026, 8, 15),
            total_hours=Decimal("160.00"),
            total_amount=Decimal("32000.00"),
        )

        self.stdout.write(self.style.SUCCESS("✓ Database seeded successfully."))
