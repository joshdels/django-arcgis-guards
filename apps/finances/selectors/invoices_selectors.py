from django.db.models import Q

from apps.finances.models import Invoice, InvoiceStatus


def get_invoices(search=None, status=None):
    invoices = Invoice.objects.select_related("billing")

    if search:
        invoices = invoices.filter(
            Q(invoice_number__icontains=search)
            | Q(billing__billing_number__icontains=search)
            | Q(billing__contract__title__icontains=search)
            | Q(billing__contract__contract_number__icontains=search)
            | Q(billing__contract__client__name__icontains=search)
            | Q(billing__contract__client__organization__icontains=search)
            | Q(billing__contract__client__client_id__icontains=search)
        )

    if status in InvoiceStatus.values:
        invoices = invoices.filter(status=status)

    return invoices
