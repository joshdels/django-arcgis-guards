from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.accounts.urls")),
    path("agency/", include("apps.agency.urls")),
    path("clients/", include("apps.client.urls")),
    path("operations/", include("apps.operations.urls")),
    path("finances/", include("apps.finances.urls")),
    path("guards/", include("apps.guard.urls")),
]
