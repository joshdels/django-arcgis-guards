from core.forms.base import CalciteModelForm
from core.forms.widgets import (
    CalciteInputWidget,
    CalciteNumberWidget,
    CalciteTextareaWidget,
)
from apps.contract.models import Contract, ContractStatus


class ClientContractForm(CalciteModelForm):
    class Meta:
        model = Contract
        fields = [
            "title",
            "description",
            "number_of_guards",
            "location",
            "start_date",
            "end_date",
        ]

        widgets = {
            "title": CalciteInputWidget(attrs={"placeholder": "Contract Title"}),
            "description": CalciteTextareaWidget(
                attrs={"placeholder": "Enter Description"}
            ),
            "number_of_guards": CalciteNumberWidget(
                attrs={"placeholder": "Enter required guards"}
            ),
            "location": CalciteNumberWidget(attrs={"placeholder": "Enter location"}),
        }

    def save(self, commit=True):
        contract = super().save(commit=False)

        if contract.pk is None:
            contract.status = ContractStatus.PENDING

        if commit:
            contract.save()

        return contract
