from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def role_required(*roles):
    """
    Decorator that restricts view access to specific roles.
    Senior Management always has access to everything.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')

            # Senior management can access everything
            if request.user.role == 'senior_management':
                return view_func(request, *args, **kwargs)

            if request.user.role in roles:
                return view_func(request, *args, **kwargs)

            messages.error(request, 'You do not have permission to access that page.')
            return redirect('dashboard-home')
        return wrapper
    return decorator