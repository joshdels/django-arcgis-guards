from django.db.models import Sum

from apps.contract.models import Contract, ContractStatus
from apps.operations.models import (
    Assignment,
    AssignmentStatus,
    Deployment,
)


def get_operations_overview():
    active_contracts = Contract.objects.filter(
        status__in=[ContractStatus.APPROVED, ContractStatus.ONGOING]
    ).count()

    active_deployments = Deployment.objects.filter(is_active=True).count()

    # Guards currently assigned.... migth review this, it should be guards that is available on on duty hehehe
    guards_assigned = Assignment.objects.filter(status=AssignmentStatus.ACTIVE).count()

    # Vacant posts = Required guards - Assigned guards
    required_guards = (
        Deployment.objects.filter(is_active=True).aggregate(
            total=Sum("required_guards")
        )["total"]
        or 0
    )

    vacant_posts = max(required_guards - guards_assigned, 0)

    return {
        "active_contracts": active_contracts,
        "active_deployments": active_deployments,
        "guards_assigned": guards_assigned,
        "vacant_posts": vacant_posts,
    }
