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


class OperationForm(forms.ModelForm):
    pass
