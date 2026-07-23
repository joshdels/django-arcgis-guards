from django.shortcuts import render


def render_client_tab(
    request,
    client,
    partial_template,
    context=None,
):
    if context is None:
        context = {}

    context.update(
        {
            "client": client,
            "current_partial": partial_template,
        }
    )

    if request.htmx:
        return render(request, partial_template, context)

    return render(
        request,
        "_client_dashboard.html",
        context,
    )
