from __future__ import annotations
from aslabs.dependencies import Dependencies as Deps
from enum import Enum
from typing import Any, Callable, Dict, Optional, List, Sequence, Type, Union, TypeVar
from fastapi import APIRouter, params, Response, routing, FastAPI, Request, utils, Depends
from fastapi.routing import APIRoute
from starlette.routing import BaseRoute
from starlette.types import ASGIApp
from fastapi.datastructures import Default
from starlette.responses import JSONResponse
import contextvars
from .resolvers import FastApiRequestResolver
from starlette.middleware.base import BaseHTTPMiddleware


class DependencyRouter(APIRouter):

    _dependency_setup: Optional[Callable[[Deps], Optional[Deps]]] = None

    def register_dependencies(self, reg: Callable[[Deps], Optional[Deps]]) -> DependencyRouter:
        self._dependency_setup = reg
        return self

    def apply_dependencies(self, deps: Deps) -> Deps:
        if self._dependency_setup is None:
            return deps

        self._dependency_setup(deps)
        return deps


dependency_context = contextvars.ContextVar(
    "dependency_context", default=Deps())


class DependencyMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, deps: Deps) -> None:
        super().__init__(app)
        self._deps = deps

    async def dispatch(self, request: Request, call_next):
        self._deps.add_resolver(FastApiRequestResolver(request))
        dependency_context.set(self._deps)
        return await call_next(request)


class Dependencies:
    def __init__(self, app: FastAPI):
        self._app = app
        self._deps = Deps()
        app.add_middleware(DependencyMiddleware, deps=self._deps)

    def register_with(self, reg: Callable[[Deps], Optional[Deps]]) -> Dependencies:
        reg(self._deps)
        return self

    def include_router(self, router: Union[APIRouter, DependencyRouter],
                       *,
                       prefix: str = "",
                       tags: Optional[List[Union[str, Enum]]] = None,
                       dependencies: Optional[Sequence[params.Depends]] = None,
                       default_response_class: Type[Response] = Default(
                           JSONResponse),
                       responses: Optional[Dict[Union[int,
                                                      str], Dict[str, Any]]] = None,
                       callbacks: Optional[List[BaseRoute]] = None,
                       deprecated: Optional[bool] = None,
                       include_in_schema: bool = True,
                       generate_unique_id_function: Callable[[APIRoute], str] = Default(
            utils.generate_unique_id
    ),) -> None:
        if isinstance(router, DependencyRouter):
            router.apply_dependencies(self._deps)
        self._app.include_router(
            router,
            prefix=prefix,
            tags=tags,
            dependencies=dependencies,
            default_response_class=default_response_class,
            responses=responses,
            callbacks=callbacks,
            deprecated=deprecated,
            include_in_schema=include_in_schema,
            generate_unique_id_function=generate_unique_id_function,
        )
        return self

    @property
    def dependencies(self):
        return self._deps


T = TypeVar("T")


def D(dependency: Type[T], *, use_cache: bool = True) -> T:
    def _resolver():
        val = dependency_context.get()
        if not isinstance(val, Deps):
            raise Exception(
                "D injector resolver must be used within request context")
        return val.get(dependency)
    return Depends(dependency=_resolver, use_cache=use_cache)


def get_dependencies() -> Deps:
    val = dependency_context.get()
    if not isinstance(val, Deps):
        raise Exception(
            "get_dependencies must be used within request context")
    return val
