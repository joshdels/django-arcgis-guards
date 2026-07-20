from core.forms.base import CalciteModelForm

from apps.finances.models import Billing


class BillingForm(CalciteModelForm):
    class Meta:
        model = Billing
        fields = [
            "contract",
            "billing_period_start",
            "billing_period_end",
            "billing_date",
            "due_date",
            "subtotal",
            "tax",
            "total_amount",
            "status",
            "remarks",
        ]


class BillingUpdateForm(CalciteModelForm):
    class Meta:
        model = Billing
        fields = [
            "contract",
            "billing_period_start",
            "billing_period_end",
            "billing_date",
            "due_date",
            "subtotal",
            "tax",
            "total_amount",
            "status",
            "is_manual",
            "remarks",
        ]
