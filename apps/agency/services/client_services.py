from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import DecimalField, Sum, Value
from django.db.models.functions import Coalesce

from apps.client.models import Client
from apps.contract.models import ContractStatus
from apps.finances.models import Invoice, Payment, Billing
from apps.guard.models import Guard, GuardStatus
from apps.operations.models import AssignmentStatus

User = get_user_model()


@transaction.atomic
def create_client(data):
    """When staff/admin adds a new client it auto creates a user auth for the client to user later"""
    contact_person = data["contact_person"].strip()
    email = data["email"].strip().lower()

    username = ".".join(contact_person.lower().split())

    original = username
    counter = 1

    while User.objects.filter(username=username).exists():
        username = f"{original}{counter}"
        counter += 1

    user = User.objects.create_user(
        username=username,
        email=email,
        password="123",
        role=User.ROLE_CLIENT,
    )

    client = Client.objects.create(
        user=user,
        name=data["name"],
        organization=data["organization"],
        location=data["location"],
        contact_person=contact_person,
        email=email,
        phone=data["phone"],
    )

    return client


def get_overview_stats(client):
    """Calculations of the guards, contracts, invoices, payments"""
    guards = Guard.objects.filter(assignments__deployment__contract__client=client)
    guards = guards.distinct()

    total_guards = guards.count()

    on_duty_guards = guards.filter(assignments__status=AssignmentStatus.ACTIVE)
    on_duty_guards = on_duty_guards.distinct()
    on_duty_guards = on_duty_guards.count()

    leave_guards = guards.filter(assignments__status=GuardStatus.LEAVE)
    leave_guards = leave_guards.distinct()
    leave_guards = leave_guards.count()

    completed_guards = guards.filter(assignments__status=AssignmentStatus.ENDED)
    completed_guards = completed_guards.distinct()
    completed_guards = completed_guards.count()

    contracts = client.contracts.all()

    active_contracts = client.contracts.filter(
        status__in=[
            ContractStatus.DRAFT,
            ContractStatus.PENDING,
            ContractStatus.APPROVED,
            ContractStatus.ONGOING,
        ]
    )

    total_contracts = contracts.count()
    total_active_contracts = active_contracts.count()
    finshed_contracts = contracts.filter(status=ContractStatus.FINISHED).count()
    cancelled_contracts = contracts.filter(status=ContractStatus.CANCELLED).count()

    total_invoices = Invoice.objects.filter(billing__contract__client=client)
    total_invoices = total_invoices.aggregate(
        total=Coalesce(
            Sum("total_amount"),
            Value(Decimal("0.00")),
            output_field=DecimalField(),
        )
    )["total"]

    total_payments = Payment.objects.filter(invoice__billing__contract__client=client)
    total_payments = total_payments.aggregate(
        total=Coalesce(
            Sum("amount"),
            Value(Decimal("0.00")),
            output_field=DecimalField(),
        )
    )["total"]

    total_balance = total_invoices - total_payments

    return {
        #contracts
        "total_contracts": total_contracts,
        "finished_contracts": finshed_contracts,
        "cancelled_contracts": cancelled_contracts,
        "total_active_contracts": total_active_contracts,
        #guards
        "total_guards": total_guards,
        "leave_guards": leave_guards,
        "on_duty_guards": on_duty_guards,
        "completed_guards": completed_guards,
        #finances
        "total_invoices": total_invoices,
        "total_payments": total_payments,
        "total_balance": total_balance,
    }


def get_client_contracts(client):
    active_contracts = client.contracts.filter(
        status__in=[
            ContractStatus.DRAFT,
            ContractStatus.PENDING,
            ContractStatus.APPROVED,
            ContractStatus.ONGOING,
        ]
    )

    history_contracts = client.contracts.filter(
        status__in=[ContractStatus.FINISHED, ContractStatus.CANCELLED]
    )

    return {
        "active_contracts": active_contracts,
        "history_contracts": history_contracts,
    }


def get_client_guards(client):
    guards = Guard.objects.filter(
        assignments__deployment__contract__client=client,
    ).distinct()

    available_guards = (
        Guard.objects.filter(
            assignments__deployment__contract__client=client,
            assignments__status=AssignmentStatus.ACTIVE,
        )
        .distinct()
        .prefetch_related("assignments")
    )

    past_guards = guards.filter(
        assignments__status__in=[
            AssignmentStatus.ENDED,
            AssignmentStatus.CANCELLED,
        ]
    ).distinct()

    return {
        "available_guards": available_guards,
        "past_guards": past_guards,
    }


def get_client_billings(client):
    billings = Billing.objects.filter(contract__client=client)

    invoices = Invoice.objects.filter(billing__contract__client=client)

    payments = Payment.objects.filter(invoice__billing__contract__client=client)

    return {
        "billings": billings,
        "invoices": invoices,
        "payments": payments,
    }
