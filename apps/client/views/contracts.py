from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from apps.accounts.decorators import roles_required
from apps.accounts.models import User
from apps.contract.models import Contract

from apps.client.forms import ClientContractForm


@roles_required("accounts:client_login", User.ROLE_CLIENT)
def contract_create(request):
    if request.method == "POST":
        form = ClientContractForm(request.POST)

        if form.is_valid():
            contract = form.save(commit=False)
            contract.client = request.user.client_profile
            contract.save()

            messages.success(request, "Contract created successfully.")
            return redirect("client_portal:overview")
    else:
        form = ClientContractForm()

    return render(
        request,
        "partials/contract/create.html",
        {"form": form},
    )


@roles_required("accounts:client_login", User.ROLE_CLIENT)
def contract_details(request, id):
    contract = get_object_or_404(Contract, id=id)

    return render(request, "partials/contract/details.html", {"contract": contract})


@roles_required("accounts:client_login", User.ROLE_CLIENT)
def contract_update(request, id):
    contract = get_object_or_404(Contract, id=id, client=request.user.client_profile)

    if request.method == "POST":
        form = ClientContractForm(request.POST, instance=contract)

        if form.is_valid():
            form.save()
            messages.success(request, "Contract updated successfully.")
            return redirect("client_portal:overview")

    else:
        form = ClientContractForm(instance=contract)

    return render(
        request,
        "partials/contract/update.html",
        {"form": form, "contract": contract},
    )


