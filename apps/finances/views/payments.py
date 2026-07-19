from django.shortcuts import render

from apps.finances.models import Payment


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