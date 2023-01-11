# pylint: disable=missing-module-docstring
from collections import namedtuple
import requests # type: ignore

Update = namedtuple("Update", ["orgnr", "change", "last_modified"])


class PagedRequestForEmbeddedList:
    """brreg api endpoint page"""

    def __init__(
        self,
        url: str,
        params: dict,
        headers: dict,
        proxies: dict,
        page_size: int,
        list_key: str,
        timeout: float,
    ) -> None:
        self.url = url
        self.headers = headers
        self.params = params
        self.proxies = proxies
        self.page_number = 0
        self.total_elements_read = 0
        self.page_size = page_size
        self.list_key = list_key
        self.timeout = timeout

    def __iter__(self):
        self.page_number = 0
        self.total_elements_read = 0
        self.params["size"] = self.page_size
        self.params["page"] = self.page_number
        return self

    def __next__(self) -> list:
        self.params["page"] = self.page_number
        response = requests.get(
            self.url,
            self.params,
            headers=self.headers,
            proxies=self.proxies,
            timeout=self.timeout,
        )
        response.raise_for_status()
        data = response.json()
        try:
            elements = data["_embedded"][self.list_key]
            assert len(elements) > 0
            self.page_number += 1
            self.total_elements_read += len(elements)
            print(
                f"{self.url}:"
                + f" found {len(elements)} on page {data['page']['number']}/{data['page']['totalPages'] - 1}"
                + f" (total: {self.total_elements_read}/{data['page']['totalElements']})"
            )
            return elements
        except (KeyError, AssertionError) as exc:
            raise StopIteration from exc
