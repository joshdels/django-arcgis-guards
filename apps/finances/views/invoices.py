from django.shortcuts import render

from apps.accounts.decorators import roles_required

from apps.accounts.models import User
from apps.finances.models import Invoice

from apps.finances.helpers import render_finances_tab


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def finances_invoices(request):
    # search = request.GET.get("search")

    invoices = Invoice.objects.select_related("billing")

    context = {"invoices": invoices}

    return render_finances_tab(request, "invoices/_invoices.html", context)


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def invoice_details(request, pk):
    invoice = Invoice.objects.select_related("billing", "billing__contract")
    invoice = invoice.get(pk=pk)

    context = {"invoice": invoice}

    return render(request, "invoices/details.html", context)


# invoice_list()

# invoice_detail()

# send_invoice()

# download_pdf()

# mark_paid()

# cancel_invoice()
