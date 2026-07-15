from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q

from apps.accounts.decorators import roles_required
from apps.accounts.models import User

from apps.contract.models import Contract


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def show_contracts(request):
    search = request.GET.get("search")

    contracts = Contract.objects.all()

    if search:
        contracts = contracts.filter(
            Q(name__icontains=search)
            | Q(organization__icontains=search)
            | Q(email__icontains=search)
        )

    context = {"contracts": contracts, "search": search}

    return render(request, "contract_page.html", context)
