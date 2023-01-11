import requests
import pandas as pd
from .browser import Crawler
from selenium import webdriver

# typing
WebElement = webdriver.remote.webelement.WebElement


class Element:
    def __init__(self,
                 crawler: Crawler,
                 value='table',
                 by='tag name',
                 **kwargs):
        self._element = crawler.element(value, by, **kwargs)

    def html(self,):
        return self._element.get_attribute('outerHTML')


class Table(Element):
    def __init__(self,
                 crawler: Crawler,
                 value='table',
                 by='tag name',
                 **kwargs):
        super().__init__(crawler, value, by, **kwargs)
        self.__raw = self._element.get_attribute('outerHTML')
        self.__data = pd.read_html(self.__raw)

    @property
    def raw(self,):
        return self.__raw

    @property
    def data(self,):
        return self.__data


class UnorderedList(Element):
    def __init__(self,
                 crawler: Crawler,
                 value='div',
                 by='tag name',
                 **kwargs):
        super().__init__(crawler, value, by, **kwargs)
        self.__parent = self._element
        self.__ul = crawler.child_of(self.__parent, "ul", "tag name")
        self.__items = crawler.children_of(self.__ul, "li", "tag name")

    @property
    def parent(self,):
        return self.__parent

    @property
    def ul(self,):
        return self.__ul

    @property
    def items(self,):
        return self.__items

    def __getitem__(self, idx: int):
        return self.__items[idx]

    def __len__(self,):
        return len(self.__items)

def download(link: str, file_name):
    response = requests.get(link.strip())
    with open(file_name, 'wb') as file:
        file.write(response.content)


def html(element: WebElement, outer=True):
    if outer:
        return element.get_attribute('outerHTML')
    else:
        return element.get_attribute('innerHTML')
