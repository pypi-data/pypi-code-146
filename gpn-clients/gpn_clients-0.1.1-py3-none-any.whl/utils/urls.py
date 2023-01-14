from abc import ABC, abstractmethod
from posixpath import join as urljoin
from typing import Dict
from urllib.parse import urlencode

from pydantic import HttpUrl, PositiveInt, parse_obj_as, validate_arguments


class AbstractURLGenerator(ABC):
    @abstractmethod
    def get_full_url(self, *args, **kwargs) -> HttpUrl:
        pass

    @abstractmethod
    def get_base_url(self) -> HttpUrl:
        pass

    @abstractmethod
    def get_full_url_with_get_params(self, *args, **kwargs) -> HttpUrl:
        pass


class URLGenerator(AbstractURLGenerator):
    @validate_arguments
    def __init__(self, host: HttpUrl, port: PositiveInt):
        self._host = host
        self._port = port

    @validate_arguments
    def get_full_url(self, path: str, *additional_paths) -> HttpUrl:
        url = urljoin(self.get_base_url(), path, *additional_paths)
        return parse_obj_as(HttpUrl, url)

    def get_base_url(self) -> HttpUrl:
        return parse_obj_as(HttpUrl, f"{self._host}:{self._port}")

    @validate_arguments
    def get_full_url_with_get_params(
            self,
            *additional_paths,
            get_params: Dict,
    ) -> HttpUrl:
        url_get_params = urlencode(get_params)
        url = urljoin(self.get_base_url(), *additional_paths)
        return parse_obj_as(HttpUrl, f"{url}?{url_get_params}")
