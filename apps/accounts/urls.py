from django.urls import path

from .views import (
    StaffLoginView,
    ClientLoginView,
    GuardLoginView,
    StaffLogoutView,
    ClientLogoutView,
    GuardLogoutView,
)

app_name = "accounts"

urlpatterns = [
    path("login/staff", StaffLoginView.as_view(), name="staff_login"),
    path("login/client", ClientLoginView.as_view(), name="client_login"),
    path("login/guard", GuardLoginView.as_view(), name="guard_login"),
    path("logout/staff", StaffLogoutView.as_view(), name="staff_logout"),
    path("logout/client", ClientLogoutView.as_view(), name="client_logout"),
    path("logout/guard", GuardLogoutView.as_view(), name="guard_logout"),
]
