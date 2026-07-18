"""
3. Assignment edit
4. Assignment deactivate
5. Deployment detail page
    |
    |-- assigned guards table
    |-- add guard button
6. Schedule/calendar later
"""

from apps.accounts.models import User
from apps.accounts.decorators import roles_required

from django.db import transaction
from django.db.models import Q

from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404

from apps.contract.models import Contract
from apps.operations.models import Deployment, Assignment

from apps.operations.helpers import render_operation_tab
from apps.operations.forms import AssignmentFormSet, DeploymentAssignmentFormSet


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def operation_assignment(request):
    search = request.GET.get("search")

    assignments = Assignment.objects.select_related(
        "guard",
        "deployment",
        "deployment__contract",
    )

    if search:
        assignments = assignments.filter(
            Q(guard__first_name__icontains=search)
            | Q(guard__last_name__icontains=search)
            | Q(guard__badge_number__icontains=search)
            | Q(deployment__name__icontains=search)
            | Q(deployment__location__icontains=search)
            | Q(deployment__contract__contract_number__icontains=search)
        )

    context = {
        "assignments": assignments,
    }

    return render_operation_tab(
        request,
        "_partials/assignment/_assignment.html",
        context,
    )


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def assignment_create_view(request):

    if request.method == "POST":
        formset = AssignmentFormSet(
            request.POST,
            queryset=Assignment.objects.none(),
        )

        if formset.is_valid():
            with transaction.atomic():
                for form in formset:
                    if not form.has_changed():
                        continue

                    form.save()

            messages.success(
                request,
                "Assignment created successfully.",
            )

            return redirect("operations:assignment_create")

    else:
        formset = AssignmentFormSet(
            queryset=Assignment.objects.none(),
        )

    context = {"formset": formset, "assignment": None}

    return render(request, "assignment/assignment_create.html", context)


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def assignment_create_deployment_view(request, deployment_id):
    deployment = get_object_or_404(
        Deployment,
        id=deployment_id,
    )

    if request.method == "POST":
        formset = DeploymentAssignmentFormSet(
            request.POST,
            instance=deployment,
        )
        
        print(formset.total_form_count())
        print(formset.initial_form_count())

        if formset.is_valid():
            with transaction.atomic():
                for form in formset:
                    if not form.has_changed():
                        continue

                    assignment = form.save(commit=False)
                    assignment.deployment = deployment
                    assignment.save()

            messages.success(
                request,
                "Assignments create successfully.",
            )

            return redirect(
                "operations:operation_assignment",
            )

    else:
        formset = DeploymentAssignmentFormSet(
            instance=deployment,
        )

    context = {"formset": formset, "deployment": deployment}

    return render(request, "assignment/assignment_create.html", context)
