from django.urls import path
from . import views

app_name = "agency"

urlpatterns = [
    path("", views.show_agency, name="home"),

    path("client-page/", views.show_clients, name="show_clients"),
    path("guard-page/", views.show_guards, name="show_guards"),
    path("contract-page/", views.show_contracts, name="show_contracts"),
    
    path("client-profile/overview/<int:id>", views.client_overview, name="client_overview"),
    path("client-profile/information/<int:id>", views.client_information, name="client_information"),
    path("client-profile/contract/<int:id>", views.client_contract, name="client_contract"),
    path("client-profile/guard/<int:id>", views.client_guard, name="client_guard"),
    path("client-profile/billing/<int:id>", views.client_billing, name="client_billing"),
    path("client-profile/report/<int:id>", views.client_report, name="client_report"),
    
    path("client-profile/<int:id>/", views.client_profile, name="client_profile"),
    path("client-profile/create/", views.client_create, name="client_create"),
    path("client-profile/update/<int:id>/", views.client_update, name="client_update"),
    path("client-profile/toggle-status/<int:id>/", views.client_toggle_status, name="client_toggle_status"),

    path("guard-profile/<int:id>/", views.guard_profile, name="guard_profile"),
    path("guard-profile/create/", views.guard_create, name="guard_create"),  
    path("guard-profile/update/<int:id>/", views.guard_update, name="guard_update"), 
    path("guard-profile/toggle-status/<int:id>", views.guard_toggle_status, name="guard_toggle_status"),
    
    path("contract-profile/<int:id>/", views.contract_profile, name="contract_profile"),
    path("contract-profile/create/", views.contract_create, name="contract_create"),
    path("contract-profile/update/<int:id>/", views.contract_update, name="contract_update"),
]