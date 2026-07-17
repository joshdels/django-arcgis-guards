from django.db.models import Prefetch

from .models import Deployment

from apps.contract.models import Contract


def deployment_list():
    return Deployment.objects.select_related("contract", "contract__client").order_by()


def deployment_detail(pk):
    return Deployment.objects.select_related("contract", "contract__client").get(pk=pk)


def deployment_by_contract(contract):
    return Deployment.objects.filter(contract=contract).order_by("name")


def active_deployment():
    return Deployment.objects.filter(is_active=True)


def contract_deployment_list():
    """
    Returns all contracts with their deployments.
    Used by the Operations > Deployments page.
    """

    return (
        Contract.objects.select_related("client")
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
