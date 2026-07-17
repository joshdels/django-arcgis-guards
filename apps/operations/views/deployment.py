from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.db import transaction
from django.db.models import Q

from apps.contract.models import Contract
from apps.operations.models import Deployment
from apps.operations.forms import ContractDeploymentForm, DeploymentFormSet


from ..selectors import (
    deployment_detail,
)
from ..services import (
    delete_deployment,
    update_deployment,
)


def deployment_create_view(request):
    if request.method == "POST":
        formset = DeploymentFormSet(
            request.POST,
            queryset=Deployment.objects.none(),
        )

        if formset.is_valid():
            with transaction.atomic():
                for form in formset:
                    if not form.has_changed():
                        continue

                    form.save()

            messages.success(
                request,
                "Deployments created successfully.",
            )

            return redirect("operations:deployment_create")

    else:
        formset = DeploymentFormSet(
            queryset=Deployment.objects.none(),
        )

    return render(
        request,
        "deployment/deployment_create.html",
        {
            "formset": formset,
            "contract": None,
        },
    )


def deployment_create_contract_view(request, contract_id):
    contract = get_object_or_404(
        Contract,
        id=contract_id,
    )

    if request.method == "POST":
        formset = DeploymentFormSet(
            request.POST,
            queryset=Deployment.objects.none(),
        )

        if formset.is_valid():
            with transaction.atomic():
                for form in formset:
                    if not form.has_changed():
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

    else:
        formset = DeploymentFormSet(
            queryset=Deployment.objects.none(),
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

    form = ContractDeploymentForm(
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

        return redirect("operations:deployment_detail", deployment.id)

    return render(
        request,
        "deployment/deployment_update.html",
        {
            "form": form,
            "deployment": deployment,
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
