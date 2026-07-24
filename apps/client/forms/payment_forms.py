from core.forms.base import CalciteModelForm

from apps.finances.models import Payment, PaymentStatus, Invoice, InvoiceStatus


class PaymentForm(CalciteModelForm):
    class Meta:
        model = Payment
        fields = [
            "invoice",
            "amount",
            "payment_method",
            "payment_date",
            "reference_number",
            "proof_of_payment",
            "remarks",
        ]

    def __init__(self, *args, invoice=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["invoice"].queryset = Invoice.objects.filter(
            status=InvoiceStatus.UNPAID
        )

        if invoice:
            self.fields["invoice"].initial = invoice
            self.fields["invoice"].disabled = True

    def save(self, commit=True):
        payment = super().save(commit=False)

        if payment.pk is None:
            payment.status = PaymentStatus.PENDING

        if commit:
            payment.save()

        return payment
