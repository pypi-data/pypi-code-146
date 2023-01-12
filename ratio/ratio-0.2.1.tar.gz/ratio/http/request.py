from ratio.http.parameters import Parameters
from http import HTTPMethod
import urllib.parse
from asgiref.typing import HTTPScope
from typing import Self


class Request:
    method: HTTPMethod
    url: str
    body: list[str]
    cookies: dict[str, str]
    fresh: bool
    path_parameters: dict[str, str]

    __parsed_url: urllib.parse.ParseResult

    def __init__(self, method: HTTPMethod, url: str) -> None:
        self.__parsed_url = urllib.parse.urlparse(url)
        self.method = method
        self.path_parameters = {}

    @property
    def url_hostname(self) -> str | None:
        return self.__parsed_url.hostname

    @property
    def url_port(self) -> int | None:
        return self.__parsed_url.port

    @property
    def url_netloc(self) -> str:
        return self.__parsed_url.netloc

    @property
    def url_path(self) -> str:
        if self.__parsed_url.path == "/":
            return "/index"

        return self.__parsed_url.path

    @property
    def protocol(self) -> str:
        return self.__parsed_url.scheme

    @property
    def query_parameters(self) -> dict[str, str | list[str]]:
        parsed_query_parameters = urllib.parse.parse_qs(self.__parsed_url.query)

        return {
            key: value[0] if len(value) == 1 else value
            for (key, value) in parsed_query_parameters.items()
        }

    @property
    def parameters(self) -> Parameters:
        return {"query": self.query_parameters, "path": self.path_parameters}

    # Reason for ignoring type: Self is actually valid. In new version of Mypy this will be supported.
    @classmethod
    def from_http_scope(cls, scope: HTTPScope) -> Self:  # type: ignore
        return cls(HTTPMethod[scope["method"]], scope["path"])
