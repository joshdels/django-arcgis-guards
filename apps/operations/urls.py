from django.urls import path
from . import views

app_name = "operations"

urlpatterns = [
    path("dashboard/", views.show_operations, name="show_operations"),
    path("dashboard/overview/", views.operation_overview, name="operation_overview"),
    path("dashboard/queue/", views.operation_queue, name="operation_queue"),
    path("dashboard/deployment/", views.operation_deployment, name="operation_deployment"),
    path("dashboard/assignment/", views.operation_assignment, name="operation_assignment"),

    path("", views.deployment_list_view, name="deployment_list"),
    path("create/", views.deployment_create_view, name="deployment_create"),
    path("<int:pk>/", views.deployment_detail_view, name="deployment_detail"),
    path("<int:pk>/edit/", views.deployment_update_view, name="deployment_update"),
    path("<int:pk>/delete/", views.deployment_delete_view, name="deployment_delete"),
]
