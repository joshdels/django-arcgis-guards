from django.db.models import Q

from apps.operations.helpers import render_operation_tab
from apps.accounts.decorators import roles_required

from apps.accounts.models import User
from apps.contract.models import Contract, ContractStatus


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def operation_queue(request):
    search = request.GET.get("search")

    contracts = Contract.objects.all()

    if search:
        contracts = contracts.filter(
            Q(contract_number__contains=search)
            | Q(client__name__icontains=search)
            | Q(client__organization__icontains=search)
        )

    contracts = (
        contracts.filter(
            status__in=[
                ContractStatus.APPROVED,
                ContractStatus.ONGOING,
            ],
            deployments__isnull=True,
        )
        .select_related("client")
        .order_by("-created_at")
    )

    context = {"contracts": contracts, "search": search}

    return render_operation_tab(request, "_partials/queue/_queue.html", context)
