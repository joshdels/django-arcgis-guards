from django import forms
from core.forms.widgets import (
    CalciteInputWidget,
    CalciteNumberWidget,
    CalciteTextareaWidget,
)

from apps.contract.models import Contract, ContractStatus
from apps.operations.models import Deployment
from django.forms import modelformset_factory


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

        widgets = {
            "name": CalciteInputWidget(attrs={"placeholder": "Deployment Name"}),
            "location": CalciteInputWidget(
                attrs={"placeholder": "Deployment Location"}
            ),
            "required_guards": CalciteNumberWidget(
                attrs={"placeholder": "Required Guards"}
            ),
            "remarks": CalciteTextareaWidget(attrs={"placeholder": "Enter remarks"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "contract" in self.fields:
            self.fields["contract"].queryset = Contract.objects.filter(
                status__in=[
                    ContractStatus.APPROVED,
                    ContractStatus.ONGOING,
                ]
            ).select_related("client")


class ContractDeploymentForm(DeploymentForm):
    class Meta(DeploymentForm.Meta):
        fields = [
            "name",
            "location",
            "required_guards",
            "remarks",
            "is_active",
        ]


DeploymentFormSet = modelformset_factory(
    Deployment,
    form=ContractDeploymentForm,
    extra=1,
    can_delete=False,
)
