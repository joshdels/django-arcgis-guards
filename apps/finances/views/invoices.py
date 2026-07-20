from django.shortcuts import render

from apps.accounts.decorators import roles_required

from apps.accounts.models import User
from apps.finances.models import Invoice

from apps.finances.helpers import render_finances_tab


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def finances_invoices(request):
    return render_finances_tab(request, "invoices/_invoices.html")


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