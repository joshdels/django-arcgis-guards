from django.db.models import Q

from apps.finances.models import Payment, PaymentStatus


def get_payments(search=None, status=None):
    payments = Payment.objects.select_related(
        "invoice",
        "invoice__billing",
    )

    if search:
        payments = payments.filter(
            Q(payment_number__icontains=search)
            | Q(reference_number__icontains=search)
            | Q(invoice__invoice_number__icontains=search)
            | Q(invoice__billing__billing_number__icontains=search)
            | Q(invoice__billing__contract__title__icontains=search)
            | Q(invoice__billing__contract__contract_number__icontains=search)
            | Q(invoice__billing__contract__client__name__icontains=search)
            | Q(invoice__billing__contract__client__organization__icontains=search)
            | Q(invoice__billing__contract__client__client_id__icontains=search)
        )

    if status in PaymentStatus.values:
        payments = payments.filter(status=status)

    return payments
