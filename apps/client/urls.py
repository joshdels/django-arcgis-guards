from django.urls import path
from . import views

app_name = "client_portal"


urlpatterns = [
    path("overview/", views.overview, name="overview"),
    path("information/", views.information, name="information"),
    path("contract/", views.client_contract, name="client_contract"),
    path("guard/", views.guard, name="guard"),
    path("finances/", views.finances, name="finances"),
    path("report/", views.report, name="report"),
    path("setting/", views.setting, name="setting"),

    path("contract/details/<int:id>/", views.contract_details, name="contract_details"),
    path("contract/create", views.contract_create, name="contract_create"),
    path("contract/update/<int:id>/", views.contract_update, name="contract_update"),

    path("payment/details/<int:pk>/", views.payment_details, name="payment_details"),
    path("payment/create/", views.payment_create, name="payment_create"),
    path("payment/create/<int:invoice_id>/", views.payment_create_invoice, name="payment_create_invoice"),
]
