"""
1. Assignment list page     <-- you are here
2. Assignment create form
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

from django.db.models import Q

from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404

from apps.contract.models import Contract
from apps.operations.models import Deployment, Assignment

from apps.operations.helpers import render_operation_tab


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
