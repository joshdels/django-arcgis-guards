from functools import wraps

from django.contrib.auth import logout
from django.shortcuts import redirect
from .utils import has_required_role


def roles_required(login_url, *roles):
    def decorator(view):
        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
            if not has_required_role(request.user, roles):
                logout(request)
                return redirect(login_url)

            return view(request, *args, **kwargs)
        return _wrapped_view
    return decorator
