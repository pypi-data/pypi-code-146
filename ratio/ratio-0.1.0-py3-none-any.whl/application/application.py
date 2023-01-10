from ratio.router.router import Router
from ratio.router.route import Route
from ratio.router.route_path import RoutePath
from ratio.http.request import Request
from ratio.http.response import Response
from ratio.application.discover_routes import discover_routes
from asgiref.typing import Scope
from http import HTTPMethod, HTTPStatus
import pathlib


class Ratio:
    application_root: pathlib.Path
    router: Router

    def __init__(self, root: pathlib.Path | None):
        self.application_root = root if root is not None else pathlib.Path(__file__)

        routes = discover_routes(self.application_root)
        self.router = Router(routes)

    async def __call__(self, scope: Scope, receive, send):
        url = scope.get("path")
        request = Request(HTTPMethod.GET, url)
        route = await self.router.resolve(request)
        response = await route()

        await send(
            {
                "type": "http.response.start",
                "status": response.code,
                "headers": [
                    [b"content-type", b"text/plain"],
                ],
            }
        )
        await send(
            {
                "type": "http.response.body",
                "body": str.encode(response.message),
            }
        )


app = Ratio(pathlib.Path.cwd())


class TestRoute(Route):
    async def get(self, request: Request) -> Response:
        return Response.from_http_status(HTTPStatus.NOT_ACCEPTABLE)


app.router.register_route(RoutePath("/"), TestRoute)
app.router.register_route(RoutePath("/test/[id]"), Route)
