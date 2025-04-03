from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def rol_requerido(*roles_permitidos):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated or request.user.rol not in roles_permitidos:
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator