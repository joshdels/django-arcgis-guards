from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from django.db.models import Q
from django.db import transaction

from apps.accounts.decorators import roles_required

from apps.accounts.models import User
from apps.finances.models import Invoice

from apps.finances.helpers import render_finances_tab
from apps.finances.forms import InvoiceForm, InvoiceUpdateForm


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def finances_invoices(request):
    search = request.GET.get("search")

    invoices = Invoice.objects.select_related("billing")

    if search:
        invoices = invoices.filter(
            Q(invoice_number__icontains=search)
            | Q(billing__billing_number__icontains=search)
            | Q(billing__contract__title__icontains=search)
            | Q(billing__contract__contract_number__icontains=search)
            | Q(billing__contract__client__name__icontains=search)
            | Q(billing__contract__client__organization__icontains=search)
            | Q(billing__contract__client__client_id__icontains=search)
        )

    context = {"invoices": invoices, "search": search}

    return render_finances_tab(request, "invoices/_invoices.html", context)


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def invoice_details(request, pk):
    invoice = Invoice.objects.select_related("billing", "billing__contract")
    invoice = invoice.get(pk=pk)

    context = {"invoice": invoice}

    return render(request, "invoices/details.html", context)


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def invoice_create(request):
    if request.method == "POST":
        form = InvoiceForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, "Invoice created successfully")

            return redirect("finances:finances_invoices")

    else:
        form = InvoiceForm()

    context = {"form": form}

    return render(request, "invoices/create.html", context)


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def invoice_edit(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)

    form = InvoiceUpdateForm(
        request.POST or None,
        instance=invoice,
    )

    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            form.save()

            messages.success(
                request,
                "Invoice update successfully.",
            )

            return redirect("finances:invoice_details", invoice.id)

    context = {"form": form, "invoice": invoice}

    return render(request, "invoices/update.html", context)
