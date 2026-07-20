from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q

from apps.finances.models import Billing
from apps.finances.forms import BillingForm, BillingUpdateForm

from apps.accounts.decorators import roles_required
from apps.accounts.models import User

from apps.finances.helpers import render_finances_tab


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def finances_billings(request):
    return render_finances_tab(request, "billings/_billings.html")


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def billing_list(request):
    billings = Billing.objects.select_related("contract", "contract__client")

    context = {"billings": billings}

    return render(request, "finance/billing.html", context)


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def billing_details(request, pk):
    billings = Billing.objects.select_related("contract", "contract__client").get(
        pk, pk
    )

    context = {"billings": billings}

    return render(request, "", context)


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def billing_create(request):
    if request.mthod == "POST":
        form = BillingForm(request.POST, queryset=Billing.objects.none())

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Billing created successfully.",
            )

            return redirect("finances:billing_create")

    else:
        form = BillingForm(
            queryset=Billing.objects.none(),
        )

    context = {"form": form, "billings": None}

    return render(request, "billing/billing_create.html", context)


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def billing_edit(request, pk):
    billing = Billing.objects.select_for_update("contract", "contract__client").get(
        pk=pk
    )

    form = BillingUpdateForm(
        request.POST or None,
        instance=billing,
    )

    if request.method == "POST" and form.is_valid():
        form.save()

        messages.success(
            request,
            "Billing update successfully.",
        )

        return redirect("finances:billing_detail", billing.id)

    context = {"form": form, "billing": billing}

    return render(request, "billing/billing_update.html", context)