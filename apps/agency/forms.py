from django import forms

from apps.client.models import Client
from apps.guard.models import Guard
from apps.contract.models import Contract


class ClientForm(forms.ModelForm):
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


class GuardForm(forms.ModelForm):
    class Meta:
        model = Guard

        fields = [
            "badge_number",
            "hourly_pay_rate",
            "address",
            "phone_number",
        ]


class ContractForm(forms.ModelForm):
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

        # for select 2 later nani
        # widgets = {
        #     "client": forms.Select(attrs={"class": "select2"}),
        #     "description": forms.Textarea(attrs={"rows": 4}),
        #     "remarks": forms.Textarea(attrs={"rows": 3}),
        #     "start_date": forms.DateInput(attrs={"type": "date"}),
        #     "end_date": forms.DateInput(attrs={"type": "date"}),
        # }
