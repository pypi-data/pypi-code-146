from fastapi import FastAPI, Request
from aslabs.dependencies import DependenciesABC, ResolverABC
from typing import Optional, TypeVar, Type

T = TypeVar("T")


class FastApiAppResolver(ResolverABC):      # TODO: add to aslabs.dependencies.fastapi
    def __init__(self, app: FastAPI) -> None:
        super().__init__()
        self._app = app

    def __call__(self, deps: DependenciesABC) -> T:
        return self._app

    @property
    def resolved_type(self) -> Type[T]:
        return FastAPI

class FastApiRequestResolver(ResolverABC):      # TODO: add to aslabs.dependencies.fastapi
    def __init__(self, app: Request) -> None:
        super().__init__()
        self._app = app

    def __call__(self, deps: DependenciesABC) -> T:
        return self._app

    @property
    def resolved_type(self) -> Type[T]:
        return Request
