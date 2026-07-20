from django.urls import path
from . import views

app_name = "finances"

urlpatterns = [
  path("", views.show_finances, name="show_finances"),
  path("overview/", views.finances_overview, name="finances_overview"),
  path("billings/", views.finances_billings, name="finances_billings"),
  path("payments/", views.finances_payments, name="finances_payments"),
  path("invoices/", views.finances_invoices, name="finances_invoices"),

  path("billing/details/<int:pk>", views.billing_details, name="billing_details"),
  path("billing/create/", views.billing_create, name="billing_create"),
  path("billing/edit/<int:pk>", views.billing_edit, name="billing_edit"),

  path("invoices/details/<int:pk>", views.invoice_details, name="invoice_details"),

  path("payments/details/<int:pk>", views.payment_details, name="payment_details"),
]