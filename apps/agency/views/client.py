from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q

from apps.accounts.decorators import roles_required
from apps.accounts.models import User

from apps.client.models import Client

from apps.agency.forms import ClientForm


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def show_clients(request):
    search = request.GET.get("search")
    status = request.GET.get("status")

    clients = Client.objects.all()

    if search:
        clients = clients.filter(
            Q(name__icontains=search)
            | Q(organization__icontains=search)
            | Q(email__icontains=search)
        )
    if status == "active":
        clients = clients.filter(is_active=True)

    elif status == "inactive":
        clients = clients.filter(is_active=False)

    return render(
        request,
        "client_page.html",
        {
            "clients": clients,
            "search": search,
            "is_active": status,
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


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def client_create(request):
    if request.method == "POST":
        form = ClientForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Client created sucessfully.")
            return redirect("agency:show_clients")
        
        print(form.errors)

    else:
        form = ClientForm()

    return render(request, "client_create.html", {"form": form})


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def client_update(request, id):
    client = get_object_or_404(Client, id=id)

    if request.method == "POST":
        form = ClientForm(request.POST, instance=client)

        if form.is_valid():
            form.save()
            messages.sucess(request, "Client updated sucessfully.")
            return redirect(
                "agency:client_profile",
                id=client.id,
            )

    else:
        form = ClientForm(instance=client)

    return render(request, "client_update.html", {"form": form, "client": client})


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def client_toggle_status(request, id):
    client = get_object_or_404(Client, id=id)
    
    client.is_active = not client.is_active
    client.save()
    
    if client.is_active:
        messages.success(
            request,
            "Client activated successfully."
        )
    else:
        messages.success(
            request,
            "Client deactivated successfully."
        )

    return redirect(
        "agency:client_profile",
        id=client.id
    )