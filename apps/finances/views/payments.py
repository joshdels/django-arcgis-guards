from django.shortcuts import render

from apps.accounts.decorators import roles_required
from apps.accounts.models import User
from apps.finances.models import Payment

from apps.finances.helpers import render_finances_tab


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def finances_payments(request):
    payments = Payment.objects.select_related(
        "invoice",
        "invoice__billing",
    )
    context = {"payments": payments}

    return render_finances_tab(request, "payments/_payments.html", context)


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def payment_details(request, pk):
    payment = Payment.objects.select_related(
        "invoice",
        "invoice__billing",
    )
    payment = payment.get(pk=pk)

    context = {"payment": payment}

    return render(request, "payments/details.html", context)
