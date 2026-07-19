from django.shortcuts import render

from apps.finances.models import Invoice


def invoice_list(request):
    invoices = Invoice.objects.select_related("client")

    context = {"invoices": invoices}

    return render(request, "finance/invoice/list.html", context)



# invoice_list()

# invoice_detail()

# send_invoice()

# download_pdf()

# mark_paid()

# cancel_invoice()