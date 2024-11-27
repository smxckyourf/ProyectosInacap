from django.contrib.auth.decorators import user_passes_test

def group_required(*group_names):
    """Decorator that checks if the user belongs to one of the specified groups."""
    def in_groups(user):
        if user.is_authenticated:
            if bool(user.groups.filter(name__in=group_names)) or user.is_superuser:
                return True
        return False
    return user_passes_test(in_groups)