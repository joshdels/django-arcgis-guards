from django.shortcuts import get_object_or_404, render

from apps.client.models import Client


def client_overview(request, id):
    client = get_object_or_404(Client, id=id)
    return render(request, "partials/content_client/overview.html", {"client": client})


def client_information(request, id):
    client = get_object_or_404(Client, id=id)
    return render(
        request, "partials/content_client/information.html", {"client": client}
    )

def client_guard(request, id):
    client = get_object_or_404(Client, id=id)
    return render(request, "partials/content_client/guard.html", {"client": client})


def client_billing(request, id):
    client = get_object_or_404(Client, id=id)
    return render(request, "partials/content_client/billing.html", {"client": client})


def client_report(request, id):
    client = get_object_or_404(Client, id=id)
    return render(request, "partials/content_client/report.html", {"client": client})
