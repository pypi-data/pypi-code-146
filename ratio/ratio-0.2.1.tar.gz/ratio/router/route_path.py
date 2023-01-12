from ratio.router.route_type import RouteType
from ratio.router.exceptions import InvalidRouteError
import re
import pathlib
from functools import cached_property
from typing import Self


ROUTE_ALLOWED_CHARACTERS = r"^[A-Za-z0-9\_\/\[\]]+$"
DYNAMIC_ROUTE_ALLOWED_CHARACTERS = r"[A-Za-z0-9\-_]+"
DYNAMIC_PATH_PARAMETER_REGEX = r"/\[[A-Za-z0-9]+\]"
INVALID_DYNAMIC_PARAMETER_REGEX = r"(.*?)\[(.*?)\/(.*?)](.*?)$"


class RoutePath:
    path: str

    def __init__(self, path: str):
        if path == "/":
            path = "/index"
        self.path = path
        self.assert_is_valid()

    # Reason for ignoring type: Self is actually valid. In new version of Mypy this will be supported.
    @classmethod
    def from_path(cls, path: pathlib.Path) -> Self:  # type: ignore
        return cls("/" + str(path))

    @property
    def route_type(self) -> RouteType:
        if len(self.parameter_keys) == 0:
            return RouteType.DIRECT

        return RouteType.DYNAMIC

    @cached_property
    def is_valid(self) -> bool:
        try:
            self.assert_is_valid()
            return True
        except InvalidRouteError:
            return False

    def assert_is_valid(self) -> None:
        if not self.path.startswith("/"):
            raise InvalidRouteError(
                "A route path should start with `/`, indicating the project root."
            )

        if self.path.endswith("/"):
            raise InvalidRouteError(
                "A route path must refer to a file, not a directory. It may not end with `/`."
            )

        if not re.match(ROUTE_ALLOWED_CHARACTERS, self.path):
            raise InvalidRouteError(
                "Routes may only contain underscores, alphanumerical characters and `/`."
            )

        if self.route_type == RouteType.DIRECT:
            return

        if not self.path.count("[") == self.path.count("]") or self.path.find(
            "["
        ) > self.path.find("]"):
            # TODO: catch /test/[id]/]id/whatever[
            raise InvalidRouteError(
                "A route with dynamic parameters should not leave open brackets."
            )

        if re.match(INVALID_DYNAMIC_PARAMETER_REGEX, self.path) is not None:
            # TODO: catch /[te/i] /[te[id]]
            raise InvalidRouteError(
                "A dynamic parameter name may not contain forward slashes."
            )

        # If a dynamic parameter key appears twice, a route is invalid
        if len(set(self.parameter_keys)) != len(self.parameter_keys):
            raise InvalidRouteError(
                "A dynamic route should contain unique parameter keys."
            )

        # For custom error routes to work, we cannot have `/[id]` as route.
        # TODO: is this really the case cause direct routes have precedence over dynamic routes
        # On the other hand, `/[id]/something` is fine.
        if len(self.parameter_keys) == 1 and len(self.path.split("/")) < 3:
            raise InvalidRouteError("Top-level dynamic routes are not allowed.")

    @cached_property
    def parameter_keys(self) -> list[str]:
        keys = re.findall(DYNAMIC_PATH_PARAMETER_REGEX, self.path)
        return [key[2:][:-1] for key in keys]

    def as_simple_regex(self) -> str:
        if self.route_type == RouteType.DIRECT:
            return self.path

        regex = self.path

        for parameter in self.parameter_keys:
            regex = re.sub(
                rf"/\[{parameter}\]", f"/({DYNAMIC_ROUTE_ALLOWED_CHARACTERS})", regex
            )

        return regex

    def as_regex(self) -> str:
        if self.route_type == RouteType.DIRECT:
            return self.path

        regex = self.path

        for parameter in self.parameter_keys:
            regex = re.sub(
                rf"/\[{parameter}\]",
                f"/(?P<{parameter}>{DYNAMIC_ROUTE_ALLOWED_CHARACTERS})",
                regex,
            )

        return regex
