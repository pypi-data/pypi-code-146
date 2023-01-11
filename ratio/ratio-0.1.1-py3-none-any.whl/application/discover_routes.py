from ratio.application.util import load_local_module, convert_snake_case_to_pascal_case
from ratio.router.route import Route
from ratio.router.route_path import RoutePath
import pathlib
from typing import Type
from enum import Enum


class RouteAction(Enum):
    ADDED = "ADDED"
    MISSING_ROUTE_CLASS = "MISSING_ROUTE_CLASS"


def guess_route_class_name(path: pathlib.Path):
    stem = path.stem
    if not stem.endswith("_route"):
        stem += "_route"

    return convert_snake_case_to_pascal_case(stem)


def map_discovered_route_to_route(
    path: pathlib.Path,
) -> tuple[Type[Route], RouteAction]:
    resolved_path = path.resolve()
    expected_class_name = guess_route_class_name(resolved_path)

    route = load_local_module("route", resolved_path)

    if not hasattr(route, expected_class_name):
        return resolved_path, RouteAction.MISSING_ROUTE_CLASS

    return resolved_path, "added"


def discover_routes(application_root: pathlib.Path) -> dict[RoutePath, Type[Route]]:
    routes_directory = application_root / "routes"
    if not routes_directory.exists() or not routes_directory.is_dir():
        return {}

    potential_routes = map(
        map_discovered_route_to_route, routes_directory.glob("**/*.py")
    )

    return {}
