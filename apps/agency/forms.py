from django import forms

from apps.client.models import Client


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