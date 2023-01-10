from os import getenv
from starlette.applications import Starlette
from starlette.routing import BaseRoute, Route
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.responses import JSONResponse

from .database import AsyncDBMiddleware
from .auth_utils import JWTAuthBackend, auth_error_handler


# Utilities
def get_required_env(var_name: str) -> str:
    var = getenv(var_name)
    if var is None:
        raise EnvironmentError(f'Could not get {var_name} from ENV')
    return var


def hasenv(var_name: str) -> bool:
    return getenv(var_name, False) is not False


def get_user(request) -> JSONResponse:
    """ Get user route """
    return JSONResponse(request.user.to_json() if request.user.is_authenticated else None)


# App factory
def create_app(routes: list[BaseRoute], secret: str, root_domain: str, database_uri: str | None, debug=False) -> Starlette:
    authbackend = JWTAuthBackend(secret)

    # Allow origins from both HTTP or HTTPS, root or subdomains, any port
    root_domain_re = r'https?://(.*\.)?{}(:\d*)?'.format(root_domain.replace('.', r'\.'))
    print('Allowed Origins Regex:', root_domain_re)

    middleware = [
        Middleware(CORSMiddleware, allow_origin_regex=root_domain_re, allow_credentials=True, allow_methods=['*']),
        Middleware(AsyncDBMiddleware, database_uri=database_uri),
        Middleware(AuthenticationMiddleware, backend=authbackend, on_error=auth_error_handler)
    ]

    app = Starlette(debug=debug, routes=routes+[Route('/getuser', get_user, methods=['GET'])], middleware=middleware)
    app.router.redirect_slashes = False
    return app
