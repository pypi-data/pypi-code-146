import abc
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, Optional, Union

import requests

from ..interfaces.context import Context
from ..interfaces.processor import Processor


class Crawler(Processor[Union[str, bytes], Union[str, bytes]]):
    def process(
        self, value: Union[str, bytes], *, context: Optional[Context] = None
    ) -> Iterable[Union[str, bytes]]:
        yield from self.crawl(value, context=context)

    @abc.abstractmethod  # type: ignore
    def crawl(
        self, location: Union[str, bytes], *, context: Optional[Context] = None
    ) -> Iterable[Any]:
        ...


@dataclass
class HTTPCrawler(Crawler):
    headers: Dict = field(default_factory=dict)

    def crawl(
        self, url: Union[str, bytes], *, context: Optional[Context] = None
    ) -> Iterable[Union[str, bytes]]:
        resp = requests.get(url, headers=self.headers)
        yield resp.content
