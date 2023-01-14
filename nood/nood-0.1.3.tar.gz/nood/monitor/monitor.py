import json
import os
import time
from abc import ABC
from threading import Thread
from typing import List, Type

from loguru import logger

from nood import api, objects
from nood.monitor.exceptions import MonitorException
from nood.monitor.parser import Parser
from nood.monitor.scraper import Scraper


class Monitor(ABC):
    def __init__(
            self,
            api_key: str,
            site_id: int,
            scraper: Type[Scraper],
            parser: Type[Parser],
            url: str = None,
            pid: str = None,
            proxies: List[objects.Proxy] = None,
            retry_intervall: int = 5,
            timeout_on_error: int = 1,
            refresh_session_on_error: bool = True,
    ):

        # init scraper and parser
        self.scraper = scraper(url=url, pid=pid, proxies=proxies)
        self.parser = parser()

        # sleep between each iteration of the run method that did not raise
        # an error
        self.retry_intervall = retry_intervall

        # sleep if an error occured
        self._timeout_on_error = timeout_on_error

        # refresh a request session within the scraper if an exception
        # is raised
        self._refresh_session_on_error = refresh_session_on_error

        # module to send products to the api
        self._ping = api.API(api_key=api_key, site_id=site_id)

    def _run(self):
        while True:
            try:
                response = self.scraper.download()
                products = self.parser.parse(response=response)
                self._ping.ping_products(products=products)
            except MonitorException:
                pass
            except TimeoutError as e:
                logger.error(f"Unknwon error occured in run method: {e}")
            finally:
                if self._refresh_session_on_error:
                    self.scraper.refresh_session()
                time.sleep(self._timeout_on_error)

    @classmethod
    def launch_tasks(
            cls,
            scraper: Type[Scraper],
            parser: Type[Parser],
            path_to_config_file: str = "config.json",
            retry_intervall: int = 5,
            timeout_on_error: int = 1,
            refresh_session_on_error: bool = True,
    ):

        # load config file
        if not os.path.exists(path_to_config_file):
            raise Exception(f"cannot find config file in path "
                            f"'{path_to_config_file}'")
        else:
            with open(path_to_config_file, "r") as f:
                config = json.load(f)
                proxies = [objects.Proxy.from_string(p)
                           for p in config.get("proxies", [])]
                logger.debug(f"loaded {len(proxies)} proxies from "
                             f"config.json")

        # launch tasks
        for url in config["urls"]:
            Thread(target=cls(
                api_key=config["apiKey"],
                site_id=config["siteId"],
                scraper=scraper,
                parser=parser,
                url=url,
                proxies=proxies,
                retry_intervall=retry_intervall,
                timeout_on_error=timeout_on_error,
                refresh_session_on_error=refresh_session_on_error
            )._run, args=()).start()
