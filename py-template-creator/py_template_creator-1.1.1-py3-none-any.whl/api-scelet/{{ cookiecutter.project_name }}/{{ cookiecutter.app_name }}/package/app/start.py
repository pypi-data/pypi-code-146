from fastapi.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
import os
from package.app import api as a_app
from package.app.schemas import (
    BaseResponseSchema,
    ValidationErrorResponseSchema,
)
import inspect
import logging
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


API_STR = os.getenv("API_ROOT", "/api")
app = None
develop = str(os.getenv("DEVELOP", "False")).lower() == "true"

logger.info("Rest API application up and running!")


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = {
        "errors": {
            err.get('loc')[-1]: err["msg"]
            for err in exc.errors()}
    }
    error_res = ValidationErrorResponseSchema(**errors)
    return JSONResponse(
        content=jsonable_encoder(error_res),
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    errors = {
        "message": exc.detail
    }
    error_res = BaseResponseSchema(**errors)
    return JSONResponse(
        content=jsonable_encoder(error_res),
        status_code=exc.status_code,
    )

allowed_hosts = os.getenv("ALLOWED_HOSTS", '*')
if allowed_hosts != '*':
    allowed_hosts = allowed_hosts.split(',')


async def exception_handler(request: Request, exc: Exception):
    response = JSONResponse(content={"message": "Internal server error."}, status_code=500)

    origin = request.headers.get('origin')

    if origin:
        # Have the middleware do the heavy lifting for us to parse
        # all the config, then update our response headers
        cors = CORSMiddleware(
                app=app,
                allow_origins=allowed_hosts,
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"])

        # Logic directly from Starlette's CORSMiddleware:
        # https://github.com/encode/starlette/blob/master/starlette/middleware/cors.py#L152

        response.headers.update(cors.simple_headers)
        has_cookie = "cookie" in request.headers

        # If request includes any cookie headers, then we must respond
        # with the specific origin instead of '*'.
        if cors.allow_all_origins and has_cookie:
            response.headers["Access-Control-Allow-Origin"] = origin

        # If we only allow specific origins, then we have to mirror back
        # the Origin header in the response.
        elif not cors.allow_all_origins and cors.is_allowed_origin(origin=origin):
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers.add_vary_header("Origin")
    return response

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=allowed_hosts if isinstance(allowed_hosts, list) else ['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
        expose_headers=['*']
    )
]

app = FastAPI(
        middleware=middleware,
        debug=False,
        exception_handlers={
            RequestValidationError: validation_exception_handler,
            HTTPException: http_exception_handler,
            Exception: exception_handler
        },
        responses={
            404: {
                "model": BaseResponseSchema
            },
            422: {
                "description": "Validation Error",
                "model": ValidationErrorResponseSchema,
            },
        },
    )

for name, obj in inspect.getmembers(a_app):
    if "_router" in name:
        app.include_router(obj, prefix=API_STR)
