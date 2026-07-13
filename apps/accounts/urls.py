from django.urls import path

from .views import (
    AdminLoginView,
    ClientLoginView,
    GuardLoginView,
    StaffLoginView,
    UserLogoutView,
)

app_name = "accounts"

urlpatterns = [
    path("admin/login/", AdminLoginView.as_view(), name="admin_login"),
    path("staff/login/", StaffLoginView.as_view(), name="staff_login"),
    path("client/login/", ClientLoginView.as_view(), name="client_login"),
    path("guard/login/", GuardLoginView.as_view(), name="guard_login"),

    path("logout/", UserLogoutView.as_view(), name="logout"),
]