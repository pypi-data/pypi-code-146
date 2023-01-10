import logging

from fastapi import FastAPI
from yente.app import request_middleware
from yente.settings import DEBUG

from . import settings
from .routers import geocode, reconcile, search, stream, xref

if DEBUG:
    logging.getLogger("ftm_columnstore").setLevel(logging.DEBUG)
else:
    logging.getLogger("ftm_columnstore").setLevel(logging.INFO)


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.TITLE,
        description=settings.DESCRIPTION,
        version=settings.VERSION,
        contact=settings.CONTACT,
        openapi_tags=settings.TAGS,
        redoc_url="/",
    )
    app.middleware("http")(request_middleware)
    app.include_router(search.router)
    app.include_router(stream.router)
    app.include_router(xref.router)
    app.include_router(geocode.router)
    app.include_router(reconcile.router)
    return app


app = create_app()
