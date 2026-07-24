from core.forms.base import CalciteModelForm

from apps.finances.models import Invoice


class InvoiceForm(CalciteModelForm):
    class Meta:
        model = Invoice
        fields = [
            "billing",
            "due_date",
            "remarks",
            "status",
        ]


class InvoiceUpdateForm(CalciteModelForm):
    class Meta:
        model = Invoice
        fields = [
            "billing",
            "due_date",
            "status",
            "remarks",
        ]
