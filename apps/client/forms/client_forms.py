from core.forms.base import CalciteModelForm
from core.forms.widgets import (
    CalciteInputWidget,
    CalciteNumberWidget,
)

from apps.client.models import Client


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
        ]

        widgets = {
            "name": CalciteInputWidget(attrs={"placeholder": "Enter client name"}),
            "organization": CalciteInputWidget(
                attrs={"placeholder": "Enter organization name"}
            ),
            "location": CalciteInputWidget(attrs={"placeholder": "Dumagete City"}),
            "contact_person": CalciteInputWidget(
                attrs={"placeholder": "Enter contact person"}
            ),
            "email": CalciteInputWidget(attrs={"placeholder": "example@email.com"}),
            "phone": CalciteNumberWidget(attrs={"placeholder": "09XXXXXXXXX"}),
        }
