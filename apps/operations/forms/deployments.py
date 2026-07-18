from django.forms import modelformset_factory

from apps.contract.models import Contract, ContractStatus
from apps.operations.models import Deployment

from core.forms.base import CalciteModelForm


class DeploymentForm(CalciteModelForm):
    class Meta:
        model = Deployment
        fields = [
            "contract",
            "name",
            "location",
            "required_guards",
            "remarks",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "contract" in self.fields:
            self.fields["contract"].queryset = Contract.objects.filter(
                status__in=[
                    ContractStatus.APPROVED,
                    ContractStatus.ONGOING,
                ]
            ).select_related("client")


class DeploymentUpdateForm(CalciteModelForm):
    class Meta:
        model = Deployment
        fields = [
            "name",
            "location",
            "required_guards",
            "remarks",
            "is_active",
        ]


class ContractDeploymentForm(DeploymentForm):
    class Meta(DeploymentForm.Meta):
        fields = [
            "name",
            "location",
            "required_guards",
            "remarks",
        ]


DeploymentFormSet = modelformset_factory(
    Deployment,
    form=ContractDeploymentForm,
    extra=1,
    can_delete=False,
)
