from typing import Iterable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from velait.velait_fastapi.api.users.services import SSOService


class UserMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        sso_service: SSOService,
        excluded_routes: Iterable = (),
        excluded_methods: Iterable[str] = (),
        *args,
        **kwargs,
    ):
        super(UserMiddleware, self).__init__(*args, **kwargs)
        self.sso_service = sso_service
        self.excluded_routes = excluded_routes
        self.excluded_methods = excluded_methods

    async def dispatch(self, request: Request, call_next):
        is_excluded_route = any(request.url.path.startswith(route) for route in self.excluded_routes)

        if is_excluded_route or request.method in self.excluded_methods:
            return await call_next(request)

        request.scope['user'] = await self.sso_service.get_user_info(
            request.headers.get('Authorization'))
        return await call_next(request)


__all__ = ['UserMiddleware']
