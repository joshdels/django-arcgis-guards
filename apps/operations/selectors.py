from .models import Deployment


def deployment_list():
    return Deployment.objects.select_related("contract", "contract__client").order_by()


def deployment_detail(pk):
    return Deployment.objects.select_related("contract", "contract__client").get(pk=pk)


def deployment_by_contract(contract):
    return Deployment.objects.filter(contract=contract).order_by("name")


def active_deployment():
    return Deployment.objects.filter(is_active=True)
