from apps.operations.helpers import render_operation_tab

from apps.accounts.decorators import roles_required

from apps.accounts.models import User
from apps.contract.models import Contract, ContractStatus


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def operation_overview(request):
    return render_operation_tab(request, "_partials/content_operation/overview.html")


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def operation_queue(request):
    contracts = (
        Contract.objects.filter(
            status__in=[
                ContractStatus.APPROVED,
                ContractStatus.ONGOING,
            ]
        )
        .select_related("client")
        .order_by("-created_at")
    )

    return render_operation_tab(
        request,
        "_partials/content_operation/queue.html",
        {
            "contracts": contracts,
        },
    )


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def operation_deployment(request):
    return render_operation_tab(request, "_partials/content_operation/deployment.html")


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def operation_assignment(request):
    return render_operation_tab(request, "_partials/content_operation/assignment.html")
