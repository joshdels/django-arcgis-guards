from django.urls import path
from . import views

app_name = "client_portal"

print(views.contract)
print(type(views.contract))

urlpatterns = [
    path("overview/", views.overview, name="overview"),
    path("information/", views.information, name="information"),
    path("contract/", views.client_contract, name="client_contract"),
    path("guard/", views.guard, name="guard"),
    path("finances/", views.finances, name="finances"),
    path("report/", views.report, name="report"),
    path("setting/", views.setting, name="setting"),

    path("contract/create", views.contract_create, name="contract_create"),
    path("contract/update/<int:id>/", views.contract_update, name="contract_update"),
]
