from django.shortcuts import get_object_or_404, render

from apps.client.models import Client
from apps.guard.models import Guard
from apps.contract.models import ContractStatus


def render_client_tab(request, id, partial_template):
    client = get_object_or_404(Client, id=id)

    contracts = client.contracts.all()

    active_contracts = client.contracts.filter(
        status__in=[
            ContractStatus.APPROVED,
            ContractStatus.ONGOING,
        ]
    )

    total_contracts = contracts.count()

    finished_contracts = contracts.filter(status=ContractStatus.FINISHED)

    cancelled_contracts = contracts.filter(status=ContractStatus.CANCELLED)

    print(active_contracts)

    guards = Guard.objects.filter(
        assignments__deployment__contract__client=client
    ).distinct()

    context = {
        "client": client,
        "contracts": contracts,
        "active_contracts": active_contracts,
        "total_contracts": total_contracts,
        "finished_contracts": finished_contracts.count(),
        "cancelled_contracts": cancelled_contracts.count(),
        "guards": guards,
        "total_guards": guards.count(),
        "active_guards": guards.filter(is_active=True).count(),
        "inactive_guards": guards.filter(is_active=False).count(),
    }

    if request.htmx:
        return render(request, partial_template, context)

    return render(request, "client/client_profile.html", context)


def render_operation_tab(request, partial_tempalte):
    if request.htmx:
        return render(request, partial_tempalte)

    return render(request, "operation/operation_page.html")
