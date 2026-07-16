from django.urls import path
from . import views

urlpatterns = [
    path(
        "deployments/",
        views.deployment_list,
        name="deployment_list",
    ),
    path(
        "deployments/create/",
        views.deployment_create,
        name="deployment_create",
    ),
    path(
        "deployments/<int:pk>/",
        views.deployment_detail,
        name="deployment_detail",
    ),
    path(
        "deployments/<int:pk>/edit/",
        views.deployment_update,
        name="deployment_update",
    ),
    path(
        "deployments/<int:pk>/delete/",
        views.deployment_delete,
        name="deployment_delete",
    ),
]
