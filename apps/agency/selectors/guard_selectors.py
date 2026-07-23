from apps.finances.models import Invoice, Payment


def get_client_invoices(client):
    return Invoice.objects.filter(billing__contract__client=client)


def get_client_payments(client):
    return Payment.objects.filter(invoice__billing__contract__client=client)
