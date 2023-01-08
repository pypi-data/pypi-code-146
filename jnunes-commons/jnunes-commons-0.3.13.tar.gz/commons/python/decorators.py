from django.shortcuts import redirect
from commons.python.utils import starts_with


def redirect_authenticated_user(redirect_to: str):
    def inner_decorator(function):
        def wrapper(request):
            if request.user.is_authenticated:
                to = redirect_to if starts_with(redirect_to, '/') else f'/{redirect_to}'
                return redirect(request.build_absolute_uri(to))
            else:
                return function(request)

        return wrapper

    return inner_decorator
