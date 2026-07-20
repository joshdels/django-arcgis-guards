from django.shortcuts import render


def render_finances_tab(request, template_name, context=None):
    context = context or {}

    if request.htmx:
        return render(request, template_name, context)

    return render(
        request,
        "_finances_page.html",
        {
            "content_template": template_name,
            **context,
        },
    )
