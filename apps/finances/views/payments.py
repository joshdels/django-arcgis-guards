from django.shortcuts import render

from apps.accounts.decorators import roles_required
from apps.accounts.models import User
from apps.finances.models import Payment

from apps.finances.helpers import render_finances_tab


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def finances_payments(request):
    return render_finances_tab(request, "payments/_payments.html")


def payment_list(request):
    payments = Payment.objects.select_related(
        "invoice",
        "invoice__client",
    )

    return render(
        request,
        "finance/payment/list.html",
        {"payments": payments},
    )


# payment_create()

# payment_detail()

# refund_payment()

# delete_payment()
