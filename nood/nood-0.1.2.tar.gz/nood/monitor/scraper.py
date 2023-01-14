import random
from abc import ABC, abstractmethod
from typing import List

import requests

from nood import objects
from nood.monitor.exceptions import MissingParameter


class Scraper(ABC):
    def __init__(
            self,
            url: str = None,
            pid: str = None,
            proxies: List[objects.Proxy] = None,
    ):
        if not url and not pid:
            raise MissingParameter("Task missing either 'url' or 'pid")

        self.url = url
        self.pid = pid

        if proxies is None:
            proxies = []
        self.proxies = proxies

        #
        self._static_proxy: objects.Proxy = self._set_static_proxy()
        self._s: requests.Session = self._set_session()

    def _set_static_proxy(self) -> objects.Proxy:
        self._static_proxy = self._chose_random_proxy()
        return self._static_proxy

    def _chose_random_proxy(self) -> objects.Proxy:
        if self.proxies:
            return random.choice(self.proxies)
        else:
            return objects.Proxy(host="", port="")

    def _set_session(self) -> requests.Session:
        self._s = requests.Session()
        self._set_static_proxy()
        return self._s

    def refresh_session(self):
        """Method to refresh the session object. This method also sets a
        new static proxy."""
        self._set_session()

    def get_random_proxy(self) -> objects.Proxy:
        """Get a random proxy chosen from the proxy list, returns proxy
        as dict for requests Session.
        """
        return self._chose_random_proxy().to_dict()

    def get_static_proxy(self) -> objects.Proxy:
        """Get a static proxy that stays the same for this instance, returns
        proxy as dict for requests Session.
        """
        if self._static_proxy is None:
            self._set_static_proxy()
        return self._static_proxy.to_dict()

    @abstractmethod
    def download(self) -> requests.Response:
        """This method must contain the programming logic to connect to a
        webserver, download and then return the response. It may contain logic
        to adapt links, make multiple requests, bypass protection, ..."""
        pass
