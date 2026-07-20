from core.forms.base import CalciteModelForm

from apps.finances.models import Payment


class PaymentForm(CalciteModelForm):
    class Meta:
        model = Payment
        fields = [
            "invoice",
            "payment_date",
            "amount",
            "payment_method",
            "reference_number",
            "status",
            "remarks",
            "proof_of_payment",
        ]


class PaymentUpdateForm(CalciteModelForm):
    class Meta:
        model = Payment
        fields = [
            "invoice",
            "payment_date",
            "amount",
            "payment_method",
            "reference_number",
            "status",
            "remarks",
            "proof_of_payment",
        ]
