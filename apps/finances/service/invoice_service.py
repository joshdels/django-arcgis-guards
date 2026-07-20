from apps.finances.models import Invoice, InvoiceStatus


def generate_invoice(billing):

    Invoice.objects.get_or_create(
        billing=billing,
        defaults={
            "due_date": billing.due_date,
            "total_amount": billing.total_amount,
            "status": InvoiceStatus.DRAFT,
        },
    )
