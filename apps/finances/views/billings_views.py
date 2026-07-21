from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from django.db.models import Q
from django.db import transaction

from apps.finances.models import Billing
from apps.finances.forms import BillingForm, BillingUpdateForm

from apps.accounts.decorators import roles_required

from apps.accounts.models import User

from apps.finances.helpers import render_finances_tab


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def finances_billings(request):
    search = request.GET.get("search")

    billings = Billing.objects.select_related("contract", "contract__client")

    if search:
        billings = billings.filter(
            Q(billing_number__icontains=search)
            | Q(contract__title__icontains=search)
            | Q(contract__contract_number__icontains=search)
            | Q(contract__client__name__icontains=search)
            | Q(contract__client__organization__icontains=search)
            | Q(contract__client__organization__icontains=search)
            | Q(contract__client__client_id__icontains=search)
        )

    context = {
        "billings": billings,
        "search": search,
    }

    return render_finances_tab(request, "billings/_billings.html", context)


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def billing_details(request, pk):
    billing = Billing.objects.select_related("contract", "contract__client").get(pk=pk)

    context = {"billing": billing}

    return render(request, "billings/details.html", context)


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def billing_create(request):
    if request.method == "POST":
        form = BillingForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                billing = form.save(commit=False)
                billing.created_by = request.user
                billing.save()

                messages.success(
                    request,
                    "Billing created successfully.",
                )

                return redirect("finances:finances_billings")

    else:
        form = BillingForm()

    context = {"form": form}

    return render(request, "billings/create.html", context)


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def billing_edit(request, billing_id):
    billing = get_object_or_404(Billing, pk=billing_id)

    form = BillingUpdateForm(
        request.POST or None,
        instance=billing,
    )

    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            form.save()

            messages.success(
                request,
                "Billing update successfully.",
            )

            return redirect("finances:billing_details", billing.id)

    context = {"form": form, "billing": billing}

    return render(request, "billings/update.html", context)
