from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from apps.accounts.decorators import roles_required

from apps.accounts.models import User
from apps.finances.models import Payment, Invoice

from apps.client.forms import PaymentForm


@roles_required("accounts:client_login", User.ROLE_CLIENT)
def payment_details(request, pk):
    payment = get_object_or_404(
        Payment.objects.select_related(
            "invoice",
            "invoice__billing",
        ),
        pk=pk,
    )

    context = {"payment": payment}

    return render(request, "partials/payments/details.html", context)


@roles_required("accounts:client_login", User.ROLE_CLIENT)
def payment_create(request):
    if request.method == "POST":
        form = PaymentForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():
            form.save()

            messages.success(request, "Payments created successfully")

            return redirect("client_portal:payment_create")

    else:
        form = PaymentForm()

    context = {"form": form}

    return render(request, "partials/payments/create.html", context)


@roles_required("accounts:client_login", User.ROLE_CLIENT)
def payment_create_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    if request.method == "POST":
        form = PaymentForm(
            request.POST,
            request.FILES,
            invoice=invoice,
        )

        if form.is_valid():
            payment = form.save(commit=False)
            payment.invoice = invoice
            payment.save()

            messages.success(request, "Payments created successfully")

            return redirect("client_portal:payment_create")

    else:
        form = PaymentForm(instance=Payment(invoice=invoice))

    context = {"form": form}

    return render(request, "partials/payments/create.html", context)
