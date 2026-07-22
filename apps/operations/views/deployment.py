from django.shortcuts import redirect, render, get_object_or_404

from django.contrib import messages

from django.db import transaction
from django.db.models import Q

from apps.accounts.models import User
from apps.contract.models import Contract
from apps.operations.models import Deployment

from apps.operations.forms import DeploymentUpdateForm, DeploymentFormSet

from apps.operations.helpers import render_operation_tab
from apps.accounts.decorators import roles_required


from ..selectors import (
    contract_deployment_list,
    deployment_detail,
)
from ..services import (
    delete_deployment,
    update_deployment,
)


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def operation_deployment(request):
    contracts, search = contract_deployment_list(request)

    

    context = {"contracts": contracts, "search": search}

    return render_operation_tab(
        request, "_partials/deployment/_deployment.html", context
    )


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def deployment_detail_view(request, pk):
    deployment = deployment_detail(pk)
    
    assignments = (
        deployment.assignments
        .select_related("guard")
        .order_by("guard__last_name", "guard__first_name")
    )

    context = {"deployment": deployment, "assignments": assignments}

    return render(request, "deployment/deployment_detail.html", context)


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
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

        context = {"formset": formset, "contract": None}

    return render(request, "deployment/deployment_create.html", context)


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
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
                "operations:operation_deployment",
            )

    else:
        formset = DeploymentFormSet(
            queryset=Deployment.objects.none(),
        )

    context = {"formset": formset, "contract": contract}

    return render(request, "deployment/deployment_create.html", context)


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def deployment_update_view(request, pk):
    deployment = deployment_detail(pk)

    form = DeploymentUpdateForm(
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

    context = {"form": form, "deployment": deployment}

    return render(request, "deployment/deployment_update.html", context)


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def deployment_delete_view(request, pk):
    deployment = deployment_detail(pk)

    if request.method == "POST":
        delete_deployment(deployment)

        messages.success(request, "Deployment deleted.")

        return redirect("operations:deployment_list")

    context = {"deployment": deployment}

    return render(request, "deployment/deployment_confirm_delete.html", context)
