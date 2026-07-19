from core.forms.base import CalciteModelForm
from apps.finances.models import Billing


# i check pa nako ni tomorrow setup sa nato
class BillingForm(CalciteModelForm):
    class Meta:
      model = Billing
      fields = [
        "contract",
        "billing_period_start",
        "billing_period_end",
        "due_date",
        "subtotal",
        "tax",
        "total_amount",
        "status",
        "is_manual",
        "remarks",
      ]
      
class BillingUpdateForm(CalciteModelForm):
    class Meta:
      model = Billing
      fields = [
        "contract",
        "billing_period_start",
        "billing_period_end",
        "due_date",
        "subtotal",
        "tax",
        "total_amount",
        "status",
        "is_manual",
        "remarks",
      ]
  