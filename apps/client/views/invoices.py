from django.shortcuts import render

from apps.accounts.decorators import roles_required

from apps.accounts.models import User
from apps.finances.models import Invoice


@roles_required("accounts:client_login", User.ROLE_CLIENT)
def invoice_details(request, pk):
    invoice = Invoice.objects.select_related("billing", "billing__contract")
    invoice = invoice.get(pk=pk)

    context = {"invoice": invoice}

    return render(request, "partials/invoices/details.html", context)
