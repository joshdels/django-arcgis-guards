from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from ..models import User


class BaseRoleLoginView(LoginView):
    """
    Base login view that only allows a specific role to log in.
    """

    required_roles = []

    def form_valid(self, form):
        response = super().form_valid(form)

        if self.request.user.role not in self.required_roles:
            logout(self.request)
            form.add_error(None, "You are not authorized to access this portal.")
            return self.form_invalid(form)

        return response


class StaffLoginView(BaseRoleLoginView):
    template_name = "staff_login.html"
    required_roles = [User.ROLE_STAFF, User.ROLE_ADMIN]
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("agency:home")


class ClientLoginView(BaseRoleLoginView):
    template_name = "client_login.html"
    required_roles = [User.ROLE_CLIENT]
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("client:dashboard")


class GuardLoginView(BaseRoleLoginView):
    template_name = "guard_login.html"
    required_roles = [User.ROLE_GUARD]
    redirect_authenticated_user = True

    def get_sucess_url(self):
        return reverse_lazy("guard:home")
