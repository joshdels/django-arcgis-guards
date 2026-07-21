from django.db.models import (
    Count,
    ExpressionWrapper,
    F,
    IntegerField,
    Q,
    Sum,
    Value,
)

from django.db.models.functions import Coalesce

from apps.contract.models import Contract, ContractStatus
from apps.guard.models import Guard
from apps.operations.models import (
    Assignment,
    AssignmentStatus,
    Deployment,
)


def get_operations_overview():
    active_contracts = Contract.objects.filter(
        status__in=[
            ContractStatus.APPROVED,
            ContractStatus.ONGOING,
        ]
    ).count()

    active_deployments = Deployment.objects.filter(is_active=True).count()

    guards_assigned = Assignment.objects.filter(status=AssignmentStatus.ACTIVE).count()

    required_guards = (
        Deployment.objects.filter(is_active=True).aggregate(
            total=Sum("required_guards")
        )["total"]
        or 0
    )

    vacant_posts = max(required_guards - guards_assigned, 0)

    recent_deployments = (
        Deployment.objects.select_related(
            "contract",
            "contract__client",
        )
        .filter(is_active=True)
        .order_by("-created_at")[:3]
    )

    requiring_more_guards = (
        Deployment.objects.filter(is_active=True)
        .select_related(
            "contract",
            "contract__client",
        )
        .annotate(
            assigned_guards=Count(
                "assignments",
                filter=Q(
                    assignments__status=AssignmentStatus.ACTIVE,
                ),
            )
        )
        .annotate(
            missing_guards=ExpressionWrapper(
                F("required_guards") - F("assigned_guards"),
                output_field=IntegerField(),
            )
        )
        .filter(
            missing_guards__gt=0,
        )
        .order_by(
            "-missing_guards",
            "contract__contract_number",
            "name",
        )
    )

    unassigned_guards = (
        Guard.objects.filter(is_active=True)
        .exclude(assignments__status=AssignmentStatus.ACTIVE)
        .distinct()
        .order_by("last_name", "first_name")[:3]
    )

    return {
        "active_contracts": active_contracts,
        "active_deployments": active_deployments,
        "guards_assigned": guards_assigned,
        "vacant_posts": vacant_posts,
        "recent_deployments": recent_deployments,
        "requiring_more_guards": requiring_more_guards,
        "unassigned_guards": unassigned_guards,
    }
