from django.shortcuts import get_object_or_404, render

from apps.client.models import Client


def client_overview(request, id):
    client = get_object_or_404(Client, id=id)
    context = {"client": client}

    if request.htmx:
        return render(request, "partials/content_client/overview.html", context)

    return render(request, "client_profile.html", context)


def client_information(request, id):
    client = get_object_or_404(Client, id=id)
    context = {"client": client}

    if request.htmx:
        return render(request, "partials/content_client/information.html", context)

    return render(request, "client_profile.html", context)

def client_contract(request, id):
    client = get_object_or_404(Client, id=id)
    context = {"client": client}

    if request.htmx:
        return render(request, "partials/content_client/contract.html", context)

    return render(request, "client_profile.html", context)


def client_guard(request, id):
    client = get_object_or_404(Client, id=id)
    context = {"client": client}

    if request.htmx:
        return render(request, "partials/content_client/guard.html", context)

    return render(request, "client_profile.html", context)


def client_billing(request, id):
    client = get_object_or_404(Client, id=id)
    context = {"client": client}

    if request.htmx:
        return render(request, "partials/content_client/billing.html", context)

    return render(request, "client_profile.html", context)


def client_report(request, id):
    client = get_object_or_404(Client, id=id)
    context = {"client": client}

    if request.htmx:
        return render(request, "partials/content_client/report.html", context)

    return render(request, "client_profile.html", context)
