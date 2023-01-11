import time
from abc import ABC

from loguru import logger

from nood import api
from nood.monitor.exceptions import MonitorException
from nood.monitor.parser import Parser
from nood.monitor.scraper import Scraper


class Monitor(ABC):
    def __init__(
            self,
            api_key: str,
            site_id: int,
            parser: Parser,
            scraper: Scraper,
            retry_intervall: int = 5,
            timeout_on_error: int = 1,
            refresh_session_on_error: bool = True
    ):
        self.parser = parser
        self.scraper = scraper

        # sleep between each iteration of the run method that did not raise
        # an error
        self.retry_intervall = retry_intervall

        # sleep if an error occured
        self._timeout_on_error = timeout_on_error

        # refresh a request session within the scraper if an exception
        # is raised
        self._refresh_session_on_error = refresh_session_on_error

        # module to send products to the api
        self._ping = api.methods.Ping(site_id=site_id, api_key=api_key)

    def run(self):
        while True:
            try:
                response = self.scraper.download()
                products = self.parser.parse(response=response)
                self._ping.products(products=products)
            except MonitorException:
                pass
            except Exception as e:
                logger.error(f"Unknwon error occured in run method: {e}")
            finally:
                if self._refresh_session_on_error:
                    self.scraper.refresh_session()
                time.sleep(self._timeout_on_error)
