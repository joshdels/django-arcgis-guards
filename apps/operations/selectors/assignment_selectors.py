from django.db.models import Q

from apps.operations.models import Assignment


def get_guard_assignments(search=None, status=None):
    assignments = Assignment.objects.select_related(
        "guard",
        "deployment",
        "deployment__contract",
        "deployment__contract__client",
    )

    if search:
        assignments = assignments.filter(
            Q(guard__first_name__icontains=search)
            | Q(guard__last_name__icontains=search)
            | Q(guard__badge_number__icontains=search)
            | Q(deployment__name__icontains=search)
            | Q(deployment__location__icontains=search)
            | Q(deployment__contract__title__icontains=search)
            | Q(deployment__contract__contract_number__icontains=search)
        )

    if status:
        assignments = assignments.filter(status=status)

    return assignments
