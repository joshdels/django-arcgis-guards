from functools import wraps

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def roles_required(login_url, *roles):
    def decorator(view):
        @login_required(login_url=login_url)
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            if request.user.role not in roles:
                logout(request)
                return redirect(login_url)

            return view(request, *args, **kwargs)

        return wrapper

    return decorator
