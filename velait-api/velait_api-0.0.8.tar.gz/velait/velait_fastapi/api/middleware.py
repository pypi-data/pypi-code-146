from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from assimilator.core.database.exceptions import InvalidQueryError, NotFoundError

from velait.common.services.search import SearchError
from velait.velait_fastapi.api.responses import APIResponse, ResponseErrorItem
from velait.velait_fastapi.api.users.exceptions import NotAuthorizedError
from velait.velait_fastapi.api.users.permissions import NoPermissionError
from velait.common.database.exceptions import AlreadyDeletedError


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
        except (NotFoundError, AlreadyDeletedError) as exc:
            return APIResponse(status_code=404, errors=[
                ResponseErrorItem(name="obj", description="Not found")
            ])
        except InvalidQueryError as exc:
            return APIResponse(status_code=400, errors=[
                ResponseErrorItem(name="obj", description="Not found")
            ])
        except NotAuthorizedError as exc:
            return APIResponse(status_code=403, errors=[
                ResponseErrorItem(name="auth", description="Not authorized")
            ])
        except NoPermissionError:
            return APIResponse(status_code=403, errors=[
                ResponseErrorItem(name="auth", description="Not enough permissions"),
            ])
        except SearchError as exc:
            return APIResponse(
                status_code=400,
                errors=[
                    ResponseErrorItem(name=error['name'], description=error['description'])
                    for error in exc.errors
                ]
            )

        return response


__all__ = [
    'ExceptionHandlerMiddleware',
]
