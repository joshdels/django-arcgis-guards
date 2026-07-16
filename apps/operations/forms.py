from django import forms

from apps.operations.models import Deployment
from apps.contract.models import Contract, ContractStatus


class DeploymentForm(forms.ModelForm):
    class Meta:
        model = Deployment
        fields = [
            "contract",
            "name",
            "location",
            "required_guards",
            "remarks",
            "is_active",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["contract"].queryset = Contract.objects.filter(
            status__in=[
                ContractStatus.APPROVED,
                ContractStatus.ONGOING,
            ]
        ).select_related("client")
