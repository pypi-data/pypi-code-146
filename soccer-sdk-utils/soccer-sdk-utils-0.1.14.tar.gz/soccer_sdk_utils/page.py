import bs4
import requests


class PageObject(object):
    _url: str
    _soup: bs4.BeautifulSoup
    _response: requests.Response
    _headers: dict | None

    def __init__(self, **kwargs):
        self.url = kwargs.get("url")
        self.soup = None
        self.response = None
        self.headers = None

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url: str):
        self._url = url

    @property
    def soup(self):
        return self._soup

    @property
    def response(self):
        return self._response

    @response.setter
    def response(self, response: requests.Response):
        self._response = response

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, headers: dict | None):
        self._headers = headers

    @soup.setter
    def soup(self, value):
        self._soup = value

    @property
    def status_code(self):
        if self.response is None:
            return None

        return self.response.status_code

    def load(self, url: str = None):
        if url is not None:
            self.url = url

        # print(f"Loading page: {self.url}")

        if self.headers is None:
            self.response = requests.get(self.url)
        else:
            self.response = requests.get(self.url, headers=self.headers)

        self.response.raise_for_status()
        self.soup = bs4.BeautifulSoup(self.response.content, "html.parser")

        return self

    def erase(self):
        self.url = None
        self.soup = None
        self.response = None

        return self

    def __repr__(self):
        return f"<PageObject(url='{self.url}')>"
