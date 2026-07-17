from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.db import transaction

from apps.contract.models import Contract
from apps.operations.models import Deployment
from apps.operations.forms import DeploymentForm, DeploymentFormSet


from ..selectors import (
    deployment_detail,
    deployment_list,
)
from ..services import (
    delete_deployment,
    update_deployment,
)


def deployment_list_view(request):
    deployments = deployment_list()

    context = {
        "deployments": deployments,
    }

    return render(request, "deployment/deployment_list.html", context)


def deployment_create_view(request, contract_id):
    contract = get_object_or_404(
        Contract,
        id=contract_id,
    )

    formset = DeploymentFormSet(
        request.POST or None,
        queryset=Deployment.objects.none(),
    )

    if request.method == "POST" and formset.is_valid():
        with transaction.atomic():
            for form in formset:
                # Skip empty forms
                if not form.cleaned_data:
                    continue

                deployment = form.save(commit=False)
                deployment.contract = contract
                deployment.save()

        messages.success(
            request,
            "Deployments created successfully.",
        )

        return redirect(
            "operations:deployment_create_contract",
            contract_id=contract.id,
        )

    return render(
        request,
        "deployment/deployment_create.html",
        {
            "formset": formset,
            "contract": contract,
        },
    )


def deployment_detail_view(request, pk):
    deployment = deployment_detail(pk)

    return render(
        request,
        "deployment/deployment_detail.html",
        {
            "deployment": deployment,
        },
    )


def deployment_update_view(request, pk):
    deployment = deployment_detail(pk)

    form = DeploymentForm(
        request.POST or None,
        instance=deployment,
    )

    if request.method == "POST" and form.is_valid():
        update_deployment(
            deployment,
            **form.cleaned_data,
        )

        messages.success(
            request,
            "Deployment updated successfully.",
        )

        return redirect("operations:deployment_list")

    return render(
        request,
        "deployment/deployment_form.html",
        {
            "form": form,
        },
    )


def deployment_delete_view(request, pk):
    deployment = deployment_detail(pk)

    if request.method == "POST":
        delete_deployment(deployment)

        messages.success(
            request,
            "Deployment deleted.",
        )

        return redirect("operations:deployment_list")

    return render(
        request,
        "deployment/deployment_confirm_delete.html",
        {
            "deployment": deployment,
        },
    )
