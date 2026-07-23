from django.db.models import Q

from apps.contract.models import Contract


def get_contracts(search=None, status=None):
    contracts = Contract.objects.all()

    if status:
        contracts = contracts.filter(status=status)

    if search:
        contracts = contracts.filter(
            Q(contract_number__icontains=search)
            | Q(title__icontains=search)
            | Q(client__name__icontains=search)
            | Q(client__organization__icontains=search)
        )

    return contracts
