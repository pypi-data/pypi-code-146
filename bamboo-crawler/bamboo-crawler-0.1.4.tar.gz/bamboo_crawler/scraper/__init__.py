import abc
import functools
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional, Union

import lxml.html

from ..interfaces.context import Context
from ..interfaces.processor import Processor


class Scraper(Processor[Union[str, bytes], Any]):
    def process(
        self, value: Union[str, bytes], *, context: Optional[Context] = None
    ) -> Iterable[Any]:
        yield from self.scrape(value, context=context)

    @abc.abstractmethod  # type: ignore
    def scrape(
        self, data: Union[str, bytes], *, context: Optional[Context] = None
    ) -> Iterable[Any]:
        ...


@dataclass
class XPathScraper(Scraper):
    xpaths: Dict[str, str]

    def scrape(
        self, data: Union[str, bytes], *, context: Optional[Context] = None
    ) -> Iterable[Dict[str, Any]]:
        elements = lxml.html.fromstring(data)
        j = {key: elements.xpath(xpath) for key, xpath in self.xpaths.items()}
        yield j


@dataclass
class SingleXPathScraper(Scraper):
    xpath: str

    def scrape(
        self, data: Union[str, bytes], *, context: Optional[Context] = None
    ) -> Iterable[Union[str, bytes]]:
        element = lxml.html.fromstring(data)
        elements = element.xpath(self.xpath)
        k = [str(x) for x in elements]  # type: ignore
        yield from k


@dataclass
class CSSSelectorScraper(Scraper):
    selectors: Dict[str, str]

    def scrape(
        self, data: Union[str, bytes], *, context: Optional[Context] = None
    ) -> Iterable[Dict[str, Any]]:
        elements = lxml.html.fromstring(data)
        j = {
            key: self.__select(elements, p_selector)
            for key, p_selector in self.selectors.items()
        }
        yield j

    def __select(
        self, elements: Any, p_selector: Union[str, bytes]
    ) -> List[str]:
        if isinstance(p_selector, (str, bytes)):
            return [e.text_content() for e in elements.cssselect(p_selector)]
        selector, attribute = p_selector
        return [e.attrib[attribute] for e in elements.cssselect(selector)]


@dataclass
class MixedHTMLScraper(Scraper):
    targets: Dict[str, Dict[str, str]] = field(default_factory=dict)

    @functools.cached_property
    def xpath_scraper(self) -> XPathScraper:
        xpaths = {
            key: target["xpath"]
            for key, target in self.targets.items()
            if "xpath" in target
        }
        return XPathScraper(xpaths=xpaths)

    @functools.cached_property
    def cssselector_scraper(self) -> CSSSelectorScraper:
        css = {
            key: target["css"]
            for key, target in self.targets.items()
            if "css" in target
        }
        return CSSSelectorScraper(selectors=css)

    def scrape(
        self, data: Union[str, bytes], *, context: Optional[Context] = None
    ) -> Iterable[Dict[str, Any]]:
        d1 = list(self.xpath_scraper.scrape(data))[0]
        d2 = list(self.cssselector_scraper.scrape(data))[0]
        yield self.__merge(d1, d2)

    def __merge(self, *scraped_data_list: Dict[str, Any]) -> Dict[str, Any]:
        d = defaultdict(list)
        for data in scraped_data_list:
            for key, values in data.items():
                d[key].extend(values)
        return dict(d)
