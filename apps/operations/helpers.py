from django.shortcuts import render


def render_operation_tab(request, template_name, context=None):
    context = context or {}

    if request.htmx:
        return render(request, template_name, context)

    return render(
        request,
        "_operation_page.html",
        {
            "content_template": template_name,
            **context,
        },
    )
