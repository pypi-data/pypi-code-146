from ..abs_source import AbsSource
from selenium import webdriver
from typing import Optional, Union, Dict
from ...tools import DriverTools
from ..df_processor import DFProcessor


# WebSource: Class for importing data from a certain web location
class WebSource(AbsSource):
    """
    This Class inherits from :class:`~Reporter.data_sources.abs_source.AbsSource`

    Basic Source template for scarping data from a web location

    Attributes
    ----------
    _driver: `webdriver`_
        the web driver used to scrape the needed source

    _driver_tools: :class:`~Reporter.tools.driver_tools.DriverTools`
        utilities for helping with webscraping using selenium
    """
    def __init__(self, driver: webdriver, post_processor: Optional[Union[Dict[str, DFProcessor], DFProcessor]] = None):
        super().__init__(post_processor)
        self._driver = driver
        self._driver_tools = DriverTools(self._driver)
