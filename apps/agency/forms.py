from core.forms.base import CalciteModelForm
from core.forms.widgets import (
    CalciteInputWidget,
    CalciteNumberWidget,
    CalciteTextareaWidget,
)

from apps.client.models import Client
from apps.guard.models import Guard
from apps.contract.models import Contract


class ClientForm(CalciteModelForm):
    class Meta:
        model = Client

        fields = [
            "name",
            "organization",
            "location",
            "contact_person",
            "email",
            "phone",
            "hourly_billing_rate",
        ]

        widgets = {
            "name": CalciteInputWidget(attrs={"placeholder": "Enter client name"}),
            "organization": CalciteInputWidget(
                attrs={"placeholder": "Enter organization name"}
            ),
            "location": CalciteInputWidget(attrs={"placeholder": "Enter location"}),
            "contact_person": CalciteInputWidget(
                attrs={"placeholder": "Enter contact person"}
            ),
            "email": CalciteInputWidget(attrs={"placeholder": "example@email.com"}),
            "phone": CalciteInputWidget(attrs={"placeholder": "09XXXXXXXXX"}),
            "hourly_billing_rate": CalciteNumberWidget(
                attrs={
                    "placeholder": "0.00",
                    "step": "1",
                }
            ),
        }


class GuardForm(CalciteModelForm):
    class Meta:
        model = Guard

        fields = [
            "first_name",
            "middle_name",
            "last_name",
            "email",
            "address",
            "email",
            "phone_number",
        ]

        widgets = {
            "first_name": CalciteInputWidget(attrs={"placeholder": "John"}),
            "middle_name": CalciteInputWidget(attrs={"placeholder": "Manigo"}),
            "last_name": CalciteInputWidget(attrs={"placeholder": "Cruz"}),
            "address": CalciteInputWidget(attrs={"placeholder": "Dumagete"}),
            "email": CalciteInputWidget(attrs={"placeholder": "john@gmail.com"}),
            "phone_number": CalciteInputWidget(attrs={"placeholder": "09XXXXXXXXX "}),
        }


class ContractForm(CalciteModelForm):

    class Meta:
        model = Contract

        fields = [
            "client",
            "title",
            "description",
            "location",
            "number_of_guards",
            "start_date",
            "end_date",
            "status",
            "remarks",
        ]

        widgets = {
            "title": CalciteInputWidget(attrs={"placeholder": "Contract Title"}),
            "description": CalciteTextareaWidget(
                attrs={"placeholder": "Enter short text"}
            ),
            "location": CalciteInputWidget(attrs={"placeholder": "Enter location"}),
            "contact_person": CalciteInputWidget(
                attrs={"placeholder": "Enter contact person"}
            ),
            "number_of_guards": CalciteInputWidget(
                attrs={"placeholder": "Enter required guards"}
            ),
            "remarks": CalciteInputWidget(attrs={"placeholder": "Enter remarks"}),
        }


class ClientContractForm(CalciteModelForm):
    class Meta:
        model = Contract
        fields = [
            "title",
            "description",
            "location",
            "number_of_guards",
            "start_date",
            "end_date",
            "status",
            "remarks",
        ]

        widgets = {
            "title": CalciteInputWidget(attrs={"placeholder": "Contract Title"}),
            "description": CalciteTextareaWidget(
                attrs={"placeholder": "Enter short text"}
            ),
            "location": CalciteInputWidget(attrs={"placeholder": "Enter location"}),
            "contact_person": CalciteInputWidget(
                attrs={"placeholder": "Enter contact person"}
            ),
            "number_of_guards": CalciteInputWidget(
                attrs={"placeholder": "Enter required guards"}
            ),
            "remarks": CalciteInputWidget(attrs={"placeholder": "Enter remarks"}),
        }
