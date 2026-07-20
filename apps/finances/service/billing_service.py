from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from apps.contract.models import Contract, BillingCycle, ContractStatus
from apps.finances.models import Billing, BillingStatus, BillingType


def generate_recurring_billings():
    """
    Generate recurring billings for active contracts.
    Intended to run daily.
    """

    today = timezone.localdate()

    contracts = Contract.objects.filter(
        is_active=True,
        status=ContractStatus.ONGOING,
    )

    for contract in contracts:

        period_start = _get_period_start(contract, today)
        period_end = _get_period_end(contract, period_start)

        exists = Billing.objects.filter(
            contract=contract,
            billing_period_start=period_start,
            billing_period_end=period_end,
        ).exists()

        if exists:
            continue

        with transaction.atomic():

            subtotal = calculate_subtotal(contract, period_start, period_end)

            tax = subtotal * contract.tax_rate / 100

            Billing.objects.create(
                contract=contract,
                billing_period_start=period_start,
                billing_period_end=period_end,
                due_date=period_end + timedelta(days=30),
                subtotal=subtotal,
                tax=tax,
                total_amount=subtotal + tax,
                status=BillingStatus.DRAFT,
            )


from calendar import monthrange
from datetime import date


def get_period(contract, today):
    """
    Returns the billing period for the current billing cycle.
    """

    if contract.billing_cycle == BillingCycle.MONTHLY:
        start = date(today.year, today.month, 1)

        last_day = monthrange(today.year, today.month)[1]

        end = date(today.year, today.month, last_day)

        return start, end

    raise NotImplementedError(f"{contract.billing_cycle} is not implemented.")


from decimal import Decimal


def calculate_subtotal(contract, start, end):
    """
    Calculate billing subtotal.
    """

    if contract.billing_type == BillingType.MONTHLY_FIXED:
        return contract.rate

    raise NotImplementedError(f"{contract.billing_type} is not implemented.")
