from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from django.db import transaction
from django.db.models import Q

from apps.accounts.decorators import roles_required

from apps.accounts.models import User
from apps.finances.models import Payment

from apps.finances.helpers import render_finances_tab
from apps.finances.forms import PaymentForm, PaymentUpdateForm


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def finances_payments(request):
    search = request.GET.get("search")

    payments = Payment.objects.select_related(
        "invoice",
        "invoice__billing",
    )

    if search:
        payments = payments.filter(
            Q(payment_number__icontains=search)
            | Q(reference_number__icontains=search)
            | Q(invoice__invoice_number__icontains=search)
            | Q(invoice__billing__billing_number__icontains=search)
            | Q(invoice__billing__contract__title__icontains=search)
            | Q(invoice__billing__contract__contract_number__icontains=search)
            | Q(invoice__billing__contract__client__name__icontains=search)
            | Q(invoice__billing__contract__client__organization__icontains=search)
            | Q(invoice__billing__contract__client__client_id__icontains=search)
        )

    context = {"payments": payments, "search": search}

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


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def payment_create(request):
    if request.method == "POST":
        form = PaymentForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():
            form.save()

            messages.success(request, "Payments created successfully")

            return redirect("finances:finances_payments")

    else:
        form = PaymentForm()

    context = {"form": form}

    return render(request, "payments/create.html", context)


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def payment_edit(request, payment_id):
    payment = get_object_or_404(Payment, pk=payment_id)

    if request.method == "POST":
        form = PaymentUpdateForm(
            request.POST,
            request.FILES,
            instance=payment,
        )

        print("VALID:", form.is_valid())
        print(form.errors)
        print(form.non_field_errors())

        if form.is_valid():
            print(form.errors.as_data())
            print(form.errors.as_json())
            
            with transaction.atomic():
                form.save()

            messages.success(request, "Payment updated successfully.")
            return redirect("finances:payment_details", pk=payment.pk)

    else:
        form = PaymentUpdateForm(instance=payment)

    return render(
        request,
        "payments/update.html",
        {
            "form": form,
            "payment": payment,
        },
    )
