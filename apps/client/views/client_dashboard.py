from django.shortcuts import render


def overview(request):
    client = request.user.client_profile
    context = {"client": client}
    
    client = request.user.client_profile
    context = {"client": client}
    
    if request.htmx:
        return render(request, "partials/content/overview.html", context)

    return render(request, "_client_dashboard.html", context)


def information(request):
    client = request.user.client_profile
    context = {"client": client}
    
    if request.htmx:
        return render(request, "partials/content/information.html", context)

    return render(request, "_client_dashboard.html", context)


def contract(request):
    client = request.user.client_profile
    context = {"client": client}
    
    if request.htmx:
        return render(request, "partials/content/contract.html", context)

    return render(request, "_client_dashboard.html", context)


def guard(request):
    client = request.user.client_profile
    context = {"client": client}
    
    if request.htmx:
        return render(request, "partials/content/guard.html", context)

    return render(request, "_client_dashboard.html", context)


def billing(request):
    client = request.user.client_profile
    context = {"client": client}
    
    if request.htmx:
        return render(request, "partials/content/billing.html", context)

    return render(request, "_client_dashboard.html", context)


def report(request):
    client = request.user.client_profile
    context = {"client": client}
    
    if request.htmx:
        return render(request, "partials/content/report.html", context)

    return render(request, "_client_dashboard.html", context)


def setting(request):
    client = request.user.client_profile
    context = {"client": client}
    
    if request.htmx:
        return render(request, "partials/content/report.html", context)

    return render(request, "_client_dashboard.html", context)
