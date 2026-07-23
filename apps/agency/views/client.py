from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q

from apps.accounts.decorators import roles_required
from apps.accounts.models import User
from apps.client.models import Client
from apps.agency.forms import ClientForm
from apps.agency.services import create_client
from apps.agency.helpers import render_client_tab
from apps.agency.selectors import get_clients
from apps.agency.services import (
    get_overview_stats,
    get_client_contracts,
    get_client_guards,
    get_client_billings,
)


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def show_clients(request):
    search = request.GET.get("search")
    status = request.GET.get("status")

    clients = Client.objects.all()

    clients = get_clients(
        search=search,
        status=status,
    )

    context = {"clients": clients, "search": search, "is_active": status}

    return render(request, "client/client_page.html", context)


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def client_overview(request, id):
    context = {}

    client = get_object_or_404(Client, id=id)

    context.update(get_overview_stats(client))
    context.update(get_client_contracts(client))

    return render_client_tab(
        request,
        client,
        "client/partial/overview.html",
        context,
    )


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def client_information(request, id):
    client = get_object_or_404(Client, id=id)

    return render_client_tab(request, client, "client/partial/information.html")


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def client_contract(request, id):
    context = {}

    client = get_object_or_404(Client, id=id)

    context.update(get_overview_stats(client))
    context.update(get_client_contracts(client))

    return render_client_tab(request, client, "client/partial/contract.html", context)


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def client_guard(request, id):
    context = {}

    client = get_object_or_404(Client, id=id)

    context.update(get_overview_stats(client))
    context.update(get_client_guards(client))

    return render_client_tab(request, client, "client/partial/guard.html", context)


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def client_finances(request, id):
    context = {}

    client = get_object_or_404(Client, id=id)

    context.update(get_overview_stats(client))
    context.update(get_client_billings(client))

    return render_client_tab(request, client, "client/partial/finances.html", context)


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def client_report(request, id):
    client = get_object_or_404(Client, id=id)

    return render_client_tab(request, client, "client/partial/report.html")


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def client_create(request):
    if request.method == "POST":
        form = ClientForm(request.POST)

        if form.is_valid():
            create_client(form.cleaned_data)

            messages.success(request, "Client created sucessfully.")
            return redirect("agency:show_clients")

    else:
        form = ClientForm()

    return render(request, "client/client_create.html", {"form": form})


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def client_update(request, id):
    client = get_object_or_404(Client, id=id)

    if request.method == "POST":
        form = ClientForm(request.POST, instance=client)

        if form.is_valid():
            form.save()
            messages.success(request, "Client updated successfully.")
            return redirect(
                "agency:client_overview",
                id=client.id,
            )

    else:
        form = ClientForm(instance=client)

    return render(
        request, "client/client_update.html", {"form": form, "client": client}
    )


@roles_required("accounts:staff_login", User.ROLE_STAFF, User.ROLE_ADMIN)
def client_toggle_status(request, id):
    client = get_object_or_404(Client, id=id)

    client.is_active = not client.is_active
    client.save()

    if client.is_active:
        messages.success(request, "Client activated successfully.")
    else:
        messages.success(request, "Client deactivated successfully.")

    return redirect("agency:client_overview", id=client.id)
