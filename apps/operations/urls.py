from django.urls import path
from . import views

app_name = "operations"

urlpatterns = [
    path("dashboard/", views.show_operations, name="show_operations"),
    path("dashboard/overview/", views.operation_overview, name="operation_overview"),
    path("dashboard/queue/", views.operation_queue, name="operation_queue"),
    path("dashboard/deployment/", views.operation_deployment, name="operation_deployment"),
    path("dashboard/assignment/", views.operation_assignment, name="operation_assignment"),

    path("deployment/create/", views.deployment_create_view, name="deployment_create"),
    path("deployment/create/<int:contract_id>/", views.deployment_create_contract_view, name="deployment_create_contract"),
    path("deployment/<int:pk>/", views.deployment_detail_view, name="deployment_detail"),
    path("deployment/edit/<int:pk>/", views.deployment_update_view, name="deployment_update"),
]
