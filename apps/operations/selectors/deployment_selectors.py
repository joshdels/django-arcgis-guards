from django.db.models import Prefetch, Q
from django.db.models import Count

from apps.operations.models import Deployment

from apps.contract.models import Contract


def contract_deployment_list(request):
    search = request.GET.get("search", "").strip()

    contracts = Contract.objects.annotate(
        assigned_guard_count=Count(
            "deployments__assignments",
            distinct=True,
        )
    )

    if search:
        contracts = contracts.filter(
            Q(contract_number__icontains=search)
            | Q(title__icontains=search)
            | Q(client__name__icontains=search)
            | Q(client__organization__icontains=search)
        )

    contracts = (
        contracts.select_related("client")
        .filter(deployments__isnull=False)
        .prefetch_related(
            Prefetch(
                "deployments",
                queryset=Deployment.objects.order_by("name"),
            )
        )
        .distinct()
        .order_by("-created_at")
    )

    return contracts, search


def deployment_detail(pk):
    return Deployment.objects.select_related("contract", "contract__client").get(pk=pk)


def deployment_by_contract(contract):
    return Deployment.objects.filter(contract=contract).order_by("name")


def active_deployment():
    return Deployment.objects.filter(is_active=True)
