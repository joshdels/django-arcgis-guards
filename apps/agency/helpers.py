from django.shortcuts import get_object_or_404, render

from apps.client.models import Client


def render_client_tab(request, id, partial_template):
    client = get_object_or_404(Client, id=id)
    context = {"client": client}

    if request.htmx:
        return render(request, partial_template, context)

    return render(request, "client/client_profile.html", context)


def render_operation_tab(request, partial_tempalte):
    if request.htmx:
        return render(request, partial_tempalte)

    return render(request, "operation/operation_page.html")
