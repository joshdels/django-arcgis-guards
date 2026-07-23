from django.db.models.functions import Coalesce
from django.db.models import (
    Count,
    F,
    IntegerField,
    OuterRef,
    Prefetch,
    Q,
    Subquery,
    Sum,
)

from apps.operations.models import Deployment, Assignment, AssignmentStatus
from apps.contract.models import Contract, ContractStatus


def get_contract_deployments(search=None, status=None, filter=None):
    required_guards = Deployment.objects.filter(
        contract=OuterRef("pk"),
    )
    required_guards = required_guards.values("contract")
    required_guards = required_guards.annotate(
        total=Sum("required_guards"),
    )
    required_guards = required_guards.values("total")

    assigned_guards = Assignment.objects.filter(
        deployment__contract=OuterRef("pk"),
        status=AssignmentStatus.ACTIVE,
    )
    assigned_guards = assigned_guards.values(
        "deployment__contract",
    )
    assigned_guards = assigned_guards.annotate(
        total=Count("pk"),
    )
    assigned_guards = assigned_guards.values("total")

    contracts = Contract.objects.filter(
        status__in=[
            ContractStatus.APPROVED,
            ContractStatus.ONGOING,
        ]
    )

    contracts = contracts.select_related("client")

    contracts = contracts.annotate(
        required_guard_count=Coalesce(
            Subquery(
                required_guards,
                output_field=IntegerField(),
            ),
            0,
        ),
        assigned_guard_count=Coalesce(
            Subquery(
                assigned_guards,
                output_field=IntegerField(),
            ),
            0,
        ),
    )

    if search:
        contracts = contracts.filter(
            Q(contract_number__icontains=search)
            | Q(title__icontains=search)
            | Q(client__name__icontains=search)
            | Q(client__organization__icontains=search)
        )

    if status:
        contracts = contracts.filter(status=status)

    if filter == "needs_guards":
        contracts = contracts.filter(
            required_guard_count__gt=F("assigned_guard_count"),
        )

    contracts = contracts.prefetch_related(
        Prefetch(
            "deployments",
            queryset=Deployment.objects.order_by("name"),
        )
    )

    contracts = contracts.order_by("-created_at")

    return contracts


def deployment_detail(pk):
    return Deployment.objects.select_related("contract", "contract__client").get(pk=pk)


def deployment_by_contract(contract):
    return Deployment.objects.filter(contract=contract).order_by("name")


def active_deployment():
    return Deployment.objects.filter(is_active=True)
