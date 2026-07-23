from decimal import Decimal

from django.shortcuts import get_object_or_404, render
from django.db.models.functions import Coalesce
from django.db.models import Sum, Value, DecimalField

from apps.client.models import Client
from apps.guard.models import Guard
from apps.contract.models import ContractStatus

from apps.finances.models import Billing, Invoice, Payment
from apps.operations.models import AssignmentStatus


# Need to optimize this soon
def render_client_tab(request, id, partial_template):
    client = get_object_or_404(Client, id=id)

    guards = Guard.objects.filter(
        assignments__deployment__contract__client=client
    ).distinct()

    available_guards = Guard.objects.filter(
        assignments__deployment__contract__client=client,
        assignments__status=AssignmentStatus.ACTIVE,
    ).prefetch_related("assignments")

    past_guards = guards.filter(
        assignments__status__in=[
            AssignmentStatus.ENDED,
            AssignmentStatus.CANCELLED,
        ]
    ).distinct

    contracts = client.contracts.all()

    total_invoices = Invoice.objects.filter(
        billing__contract__client=client
    ).aggregate(
        total=Coalesce(
            Sum("total_amount"),
            Value(Decimal("0.00")),
            output_field=DecimalField(),
        )
    )["total"]

    total_payments = Payment.objects.filter(
        invoice__billing__contract__client=client
    ).aggregate(
        total=Coalesce(
            Sum("amount"),
            Value(Decimal("0.00")),
            output_field=DecimalField(),
        )
    )["total"]

    total_balance = total_invoices - total_payments

    active_contracts = client.contracts.filter(
        status__in=[
            ContractStatus.DRAFT,
            ContractStatus.PENDING,
            ContractStatus.APPROVED,
            ContractStatus.ONGOING,
        ]
    )

    history_contracts = client.contracts.filter(
        status__in=[
            ContractStatus.FINISHED,
            ContractStatus.CANCELLED,
        ]
    )

    total_contracts = contracts.count()

    finished_contracts = contracts.filter(status=ContractStatus.FINISHED)

    cancelled_contracts = contracts.filter(status=ContractStatus.CANCELLED)

    billings = Billing.objects.filter(contract__client=client)

    invoices = Invoice.objects.filter(billing__contract__client=client)

    payments = Payment.objects.filter(invoice__billing__contract__client=client)

    context = {
        "client": client,
        "contracts": contracts,
        "active_contracts": active_contracts,
        "history_contracts": history_contracts,
        "total_contracts": total_contracts,
        "finished_contracts": finished_contracts.count(),
        "cancelled_contracts": cancelled_contracts.count(),
        "guards": guards,
        "total_guards": guards.count(),
        "active_guards": guards.filter(is_active=True).count(),
        "inactive_guards": guards.filter(is_active=False).count(),
        # Finance
        "billings": billings,
        "invoices": invoices,
        "payments": payments,
        "client": client,
        "current_partial": partial_template,
        "available_guards": available_guards,
        "past_guards": past_guards,
        # total finances
        "total_invoices": total_invoices,
        "total_payments": total_payments,
        "total_balance": total_balance
    }
    

    if request.htmx:
        return render(request, partial_template, context)

    return render(request, "client/client_profile.html", context)
