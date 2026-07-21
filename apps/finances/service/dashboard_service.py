from decimal import Decimal

from django.db.models import Sum
from django.db.models.functions import TruncMonth

from apps.finances.models import Billing, Invoice, Payment, InvoiceStatus


def get_finance_overview():
    labels = []
    totals = []

    total_billings = Billing.objects.aggregate(total=Sum("total_amount"))[
        "total"
    ] or Decimal("0.00")

    total_invoices = Invoice.objects.aggregate(total=Sum("total_amount"))[
        "total"
    ] or Decimal("0.00")

    total_payments = Payment.objects.aggregate(total=Sum("amount"))["total"] or Decimal(
        "0.00"
    )

    monthly_revenue = (
        Payment.objects.annotate(month=TruncMonth("payment_date"))
        .values("month")
        .annotate(total=Sum("amount"))
        .order_by("month")
    )

    for row in monthly_revenue:
        labels.append(row["month"].strftime("%b %Y"))
        totals.append(float(row["total"]))

    recent_billings = Billing.objects.select_related(
        "contract", "contract__client"
    ).order_by("-created_at")[:3]

    upcoming_invoices = (
        Invoice.objects.select_related(
            "billing",
            "billing__contract",
            "billing__contract__client",
        )
        .exclude(status=InvoiceStatus.PAID)
        .order_by("due_date")[:3]
    )

    recent_payments = Payment.objects.select_related(
        "invoice",
        "invoice__billing",
        "invoice__billing__contract",
        "invoice__billing__contract__client",
    ).order_by("-payment_date")[:3]

    return {
        "total_billings": total_billings,
        "total_invoices": total_invoices,
        "total_payments": total_payments,
        "outstanding": total_invoices - total_payments,
        "revenue_labels": labels,
        "revenue_totals": totals,
        "recent_billings": recent_billings,
        "upcoming_invoices": upcoming_invoices,
        "recent_payments": recent_payments,
    }
