from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from apps.accounts.decorators import roles_required
from apps.accounts.models import User

from apps.client.models import Client


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def show_clients(request):
    search = request.GET.get("search")

    clients = Client.objects.all()

    if search:
        clients = clients.filter(
            Q(name__icontains=search)
            | Q(organization__icontains=search)
            | Q(email__icontains=search)
        )

    return render(
        request,
        "client_page.html",
        {
            "clients": clients,
            "search": search,
        },
    )


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def client_profile(request, id):
    client = get_object_or_404(Client, id=id)

    return render(
        request,
        "client_profile.html",
        {
            "client": client,
        },
    )
