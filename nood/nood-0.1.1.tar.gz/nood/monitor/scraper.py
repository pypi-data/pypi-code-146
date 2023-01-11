import random
from abc import ABC, abstractmethod

import requests

from nood import objects
from nood.monitor.exceptions import MissingParameter


class Scraper(ABC):
    def __init__(
            self,
            url: str = None,
            pid: str = None,
            proxies: list[objects.Proxy] = list,
    ):
        if not url and not pid:
            raise MissingParameter("Task missing either 'url' or 'pid")

        self.url = url
        self.pid = pid
        self.proxies = proxies

        #
        self._static_proxy: objects.Proxy = self._set_static_proxy()
        self._s: requests.Session = self._set_session()

    def _set_static_proxy(self) -> objects.Proxy:
        self._static_proxy = self.get_random_proxy()
        return self._static_proxy

    def _set_session(self) -> requests.Session:
        self._s = requests.Session()
        self._set_static_proxy()
        return self._s

    def refresh_session(self):
        """Method to refresh the session object. This method also sets a
        new static proxy."""
        self._set_session()

    def get_random_proxy(self) -> objects.Proxy:
        """Get a random proxy chosen from the proxy list.
        """
        return random.choice(self.proxies)

    def get_static_proxy(self) -> objects.Proxy:
        """Get a static proxy that stays the same for this instance.
        """
        if self._static_proxy is None:
            self._set_static_proxy()
        return self._static_proxy

    @abstractmethod
    def download(self) -> requests.Response:
        """This method must contain the programming logic to connect to a
        webserver, download and then return the response. It may contain logic
        to adapt links, make multiple requests, bypass protection, ..."""
        pass


import json
import time
from dataclasses import dataclass
from typing import List, Optional

from threading import Thread

# custom package
from monitor.webhook import Webhook
from monitor.database import Database
from monitor.logger import Logger
from monitor.proxies import Proxies
from monitor.config import Config
from monitor.color import Color

# custom package
import tls_requests

log: Logger = Logger()


@dataclass
class Product:
    name: Optional[str]
    url: Optional[str]
    image: Optional[str]
    product_id: Optional[str]
    product_sizes: Optional[List[str]]
    is_available: Optional[bool]
    is_raffle_product: Optional[bool]

    @classmethod
    def load_from_json(cls, data: dict):
        return Product(
            name=cls.__get_product_name(data),
            url=cls.__get_product_url(cls.__get_product_id(data)),
            image=cls.__get_product_image(data),
            product_id=cls.__get_product_id(data),
            product_sizes=cls.__get_product_sizes(data),
            is_available=cls.__is_available(data),
            is_raffle_product=cls.__is_raffle_product(data)
        )

    @staticmethod
    def __is_raffle_product(data: dict) -> Optional[bool]:
        return data['product'].get('isRaffleProduct')

    @staticmethod
    def __is_available(data: dict) -> Optional[bool]:
        return data['product'].get('available')

    @staticmethod
    def __get_product_image(data: dict) -> Optional[str]:
        return \
            data['product']['images']['large'][0]['sources'][0][
                'srcset'].split(
                ",")[0]

    @staticmethod
    def __get_product_name(data: dict) -> Optional[str]:
        return data['product'].get('productName')

    @staticmethod
    def __get_product_id(data: dict) -> Optional[str]:
        return data['product'].get('id')

    @staticmethod
    def __get_product_url(pid: Optional[str]) -> Optional[str]:
        if pid:
            return f"https://www.kickz.com/en/p/xxx/{pid}.html"

    @staticmethod
    def __get_product_sizes(data: dict) -> Optional[List[str]]:
        z: List[str] = []
        for x in data['product']['variationAttributes']:
            if x.get('id') == 'size':
                for y in x['values']:
                    if y.get('graySoldOutSizes'):
                        z.append(y['id'])

        return z


class Monitor:
    def __init__(self, _config: Config, _product: str):
        self.config: Config = config
        self.color: Color = Color()
        self.product: str = _product
        self.product_url: str = self.__get_product_url(_product)
        self.webhook: Webhook = Webhook(
            self.config.webhook,
            ping_products_immediately=False
        )
        self.proxies: Proxies = Proxies.load_from_txt()
        self.proxy: dict = self.proxies.random_proxy_dict
        self.timestamp: float = time.time()
        self.session: tls_requests.Session = self.__gen_session()

        self.database: Database = Database("kickz.db")
        self.database.create_database()
        self.database.clear()

    def __get_product_url(self, _product: str) -> str:
        return "".join(
            [
                "https://www.kickz.com/on/demandware.store/Sites-Kickz-DE-AT-INT-Site",
                f"/de_DE/Product-Variation?dwvar_{_product}_",
                f"color={self.color.random_color}&pid={_product}&quantity=1&ajax=true"
            ]
        )

    def __gen_session(self) -> tls_requests.Session:
        self.session = tls_requests.Session(http2=True)
        self.proxy = self.proxies.random_proxy_dict
        self.timestamp = time.time()

        try:
            self.session.get("https://www.kickz.com", proxies=self.proxy,
                             timeout=10)
        except Exception as _:
            pass

        return self.session

    def __validate_session(self) -> None:
        if int(time.time()) >= int(self.timestamp + 180):
            log.info("Generating new session")
            self.session = self.__gen_session()

    def run(self) -> None:
        while True:
            try:
                self.__validate_session()

                response = self.session.options(
                    self.product_url,
                    proxies=self.proxy,
                    timeout=10,
                )

                if response.status_code != 200:
                    log.info(
                        f"{response.status_code} failed request to {self.product}")
                    self.session = self.__gen_session()
                    time.sleep(0.5)
                    continue

                _product: Product = Product.load_from_json(
                    json.loads(response.text))

                if not _product.is_available:
                    log.info(
                        f"{response.status_code} product not in stock {self.product}")
                    time.sleep(self.config.delay)
                    continue

                if _product.is_raffle_product:
                    log.info(
                        f"{response.status_code} product is raffle product {self.product}")
                    time.sleep(self.config.delay)
                    continue

                if self.database.is_new_database_change(url=_product.url):
                    self.webhook.send(
                        store="Kickz",
                        product_url=_product.url,
                        product_name=_product.name,
                    )

                if self.database.is_new_database_change(
                        url=_product.url,
                        product_sizes=_product.product_sizes,
                        positive_changes_only=True
                ):
                    log.info(
                        f"new restock {self.product} {_product.product_sizes}")
                    self.webhook.send(
                        store="Kickz",
                        product_url=_product.url,
                        product_name=_product.name,
                        sizes=_product.product_sizes,
                    )

                log.info(f"{response.status_code} checked {_product.name}")
                time.sleep(self.config.delay)

            except Exception as e:
                log.error(f"error {e} {self.product}")
                self.session = self.__gen_session()
                time.sleep(0.5)


if __name__ == '__main__':
    config: Config = Config.load_from_json()

    for _, product in enumerate(config.products):
        monitor = Monitor(config, product)
        t = Thread(target=monitor.run, args=())
        t.start()
