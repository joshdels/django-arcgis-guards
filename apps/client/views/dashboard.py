from django.shortcuts import render

from apps.accounts.decorators import roles_required
from apps.accounts.models import User

from apps.agency.services import (
    get_overview_stats,
    get_client_contracts,
    get_client_guards,
    get_client_billings,
)

from apps.client.selectors import get_client_information
from apps.client.helpers import render_client_tab


@roles_required("accounts:client_login", User.ROLE_CLIENT)
def overview(request):
    context = {}

    client = request.user.client_profile

    context.update(get_client_information(client))
    context.update(get_overview_stats(client))
    context.update(get_client_contracts(client))

    return render_client_tab(request, client, "partials/content/overview.html", context)


@roles_required("accounts:client_login", User.ROLE_CLIENT)
def information(request):
    context = {}

    client = request.user.client_profile
    context.update(get_client_information(client))

    return render_client_tab(
        request, client, "partials/content/information.html", context
    )


@roles_required("accounts:client_login", User.ROLE_CLIENT)
def client_contract(request):
    context = {}

    client = request.user.client_profile
    context.update(get_client_information(client))
    context.update(get_client_contracts(client))
    context.update(get_overview_stats(client))

    if request.htmx:
        return render(request, "partials/content/contract.html", context)

    return render(request, "_client_dashboard.html", context)


@roles_required("accounts:client_login", User.ROLE_CLIENT)
def guard(request):
    context = {}

    client = request.user.client_profile
    context.update(get_client_information(client))
    context.update(get_client_guards(client))
    context.update(get_overview_stats(client))

    return render_client_tab(request, client, "partials/content/guard.html", context)


@roles_required("accounts:client_login", User.ROLE_CLIENT)
def finances(request):
    context = {}

    client = request.user.client_profile
    context.update(get_client_information(client))
    context.update(get_client_billings(client))
    context.update(get_overview_stats(client))

    return render_client_tab(request, client, "partials/content/finances.html", context)


@roles_required("accounts:client_login", User.ROLE_CLIENT)
def report(request):
    client = request.user.client_profile
    context = {"client": client}

    return render_client_tab(request, client, "partials/content/report.html", context)


@roles_required("accounts:client_login", User.ROLE_CLIENT)
def setting(request):
    client = request.user.client_profile
    context = {"client": client}

    return render_client_tab(request, client, "partials/content/setting.html", context)
