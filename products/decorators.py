from django.http import HttpResponseForbidden
from functools import wraps
def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(view_instance, request, *args, **kwargs):
            user = request.user
            # Ensure the user is authenticated
            if not user.is_authenticated:
                return HttpResponseForbidden("You must be logged in to access this page.")
            
            # Check if the user has a valid role
            if not hasattr(user, 'role') or user.role not in allowed_roles:
                return HttpResponseForbidden("You do not have permission to access this page.")

            return view_func(view_instance, request, *args, **kwargs)
        return _wrapped_view
    return decorator