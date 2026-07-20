from django.urls import path
from . import views

app_name = "finances"

urlpatterns = [
  path("", views.show_finances, name="show_finances"),
  path("overview/", views.finances_overview, name="finances_overview"),
  path("billings/", views.finances_billings, name="finances_billings"),
  path("payments/", views.finances_payments, name="finances_payments"),
  path("invoices/", views.finances_invoices, name="finances_invoices"),
]