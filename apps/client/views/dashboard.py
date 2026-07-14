from django.shortcuts import render

from apps.accounts.decorators import roles_required
from apps.accounts.models import User


@roles_required("accounts:client_login", User.ROLE_CLIENT)
def dashboard(request):
    client = request.user.client_profile

    context = {"client": client}

    return render(request, "_client_dashboard.html", context)
