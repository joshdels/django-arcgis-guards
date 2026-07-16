from django.contrib import messages
from django.shortcuts import redirect, render

from ..forms import DeploymentForm

from ..selectors import (
    deployment_detail,
    deployment_list,
)
from ..services import (
    create_deployment,
    delete_deployment,
    update_deployment,
)


def deployment_list_view(request):
    deployments = deployment_list()

    context = {
        "deployments": deployments,
    }

    return render(request, "deployment/deployment_list.html", context)


def deployment_create_view(request):
    form = DeploymentForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        create_deployment(**form.cleaned_data)

        messages.success(
            request,
            "Deployment created successfully.",
        )

        return redirect("deployment_list")

    return render(
        request,
        "deployment/deployment_form.html",
        {
            "form": form,
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

        return redirect("deployment_list")

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

        return redirect("deployment_list")

    return render(
        request,
        "deployment/deployment_confirm_delete.html",
        {
            "deployment": deployment,
        },
    )
