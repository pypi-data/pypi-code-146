"""
This module provides core page object functionality.
"""
import bs4
import requests


class PageObject:
    """
    The PageObject class is the base class for all page objects. It provides the
    basic functionality to load a page and to extract data from the page.
    """

    def __init__(self, **kwargs):
        self.url = kwargs.get("url")
        self.soup = None
        self.response = None
        self.headers = None

    @property
    def url(self):
        """
        The url property returns the url of the page.
        """
        return self._url

    @url.setter
    def url(self, url: str):
        """
        The url setter validates the url and sets the url property.
        """
        self._url = url

    @property
    def soup(self):
        """
        The soup property returns the BeautifulSoup object of the page.
        """
        return self._soup

    @property
    def response(self):
        """
        The response property returns the response object of the page.
        """
        return self._response

    @response.setter
    def response(self, response: requests.Response):
        """
        The response setter validates the response object and sets the response
        """
        self._response = response

    @soup.setter
    def soup(self, value):
        """
        The soup setter validates the soup object and sets the soup property.
        """
        self._soup = value

    @property
    def status_code(self):
        """
        The status_code property returns the status code of the response.
        """
        if self.response is None:
            return None

        return self.response.status_code

    def load(self, url: str = None):
        """
        The load method loads the page and returns the response object.
        """
        if self.url is None and url is None:
            raise ValueError("The url parameter is required!")

        if url is not None:
            self.url = url

        # print(f"Loading page: {self.url}")

        if self.headers is None:
            self.response = requests.get(self.url, timeout=10)
        else:
            self.response = requests.get(self.url, headers=self.headers, timeout=10)

        self.response.raise_for_status()
        self.soup = bs4.BeautifulSoup(self.response.content, "html.parser")

        return self

    def erase(self):
        """
        The erase method erases the page object.
        """
        self.url = None
        self.soup = None
        self.response = None
        self.headers = None

        return self

    def __repr__(self):
        return f"PageObject(url='{self.url}')"
