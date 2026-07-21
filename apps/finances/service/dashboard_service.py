from decimal import Decimal
from django.db.models import Sum

from apps.finances.models import Billing, Invoice, Payment


def get_finance_overview():
    total_billings = Billing.objects.aggregate(total=Sum("total_amount"))[
        "total"
    ] or Decimal("0.00")

    total_invoices = Invoice.objects.aggregate(total=Sum("total_amount"))[
        "total"
    ] or Decimal("0.00")

    total_payments = Payment.objects.aggregate(total=Sum("amount"))["total"] or Decimal(
        "0.00"
    )

    return {
        "total_billings": total_billings,
        "total_invoices": total_invoices,
        "total_payments": total_payments,
        "outstanding": total_invoices - total_payments,
    }
