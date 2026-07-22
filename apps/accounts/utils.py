def has_required_role(user, allowed_roles):
    """Returns True if the user has one of the allowed roles"""

    if not user.is_authenticated:
        return False
    return user.role in allowed_roles
