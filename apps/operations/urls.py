from django.urls import path
from . import views

app_name = "operations"

urlpatterns = [
    path("overview/", views.operation_overview, name="operation_overview"),
    path("queue/", views.operation_queue, name="operation_queue"),
    path("deployment/", views.operation_deployment, name="operation_deployment"),
    path("assignment/", views.operation_assignment, name="operation_assignment"),

    path("deployment/create/", views.deployment_create_view, name="deployment_create"),
    path("deployment/create/<int:contract_id>/", views.deployment_create_contract_view, name="deployment_create_contract"),
    path("deployment/<int:pk>/", views.deployment_detail_view, name="deployment_detail"),
    path("deployment/edit/<int:pk>/", views.deployment_update_view, name="deployment_update"),
    
    path("assignment/create/", views.assignment_create_view, name="assignment_create"),
    path("assignment/create/<int:deployment_id>/", views.assignment_create_deployment_view, name="assignment_create_deployment"),
    path("assignment/<int:pk>/", views.assignment_detail_view, name="assignment_detail_view"),
    path("assignment/edit/<int:pk>/", views.assignment_edit_view, name="assignment_edit_view"),
]
