"""Utils for reading remote files."""
import json
import logging
import ssl
import time
from warnings import warn

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from utils import File, filex, timex, tsv
from utils.browserx import Browser
from utils.cache import cache

USER_AGENT = (
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) '
    + 'Gecko/20100101 Firefox/65.0'
)
ENCODING = 'utf-8'
SELENIUM_SCROLL_REPEATS = 3
SELENIUM_SCROLL_WAIT_TIME = 0.5
EXISTS_TIMEOUT = 1

# pylint: disable=W0212
ssl._create_default_https_context = ssl._create_unverified_context


class WWW:
    def __init__(self, url: str):
        self.url = url

    def readBinary(self):
        try:
            resp = requests.get(self.url, headers={'user-agent': USER_AGENT})
            if resp.status_code != 200:
                raise Exception(
                    f'Failed to read {self.url}. resp.status_code != 200. '
                )
            content = resp.content
            content_size = len(content)
            if content_size == 0:
                raise Exception(
                    f'Failed to read {self.url}. content_size == 0.'
                )
            return content
        except requests.exceptions.ConnectionError as e:
            raise Exception(f'Failed to read {self.url}. {e}')

    def readSelenium(self):
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options)
        driver.get(self.url)
        content = driver.page_source
        driver.quit()
        return content

    def read(self):
        return self.readBinary().decode()

    def readJSON(self):
        content = self.read()
        return json.loads(content) if content else None

    def readXSV(self, separator):
        content = self.read()
        return tsv._read_helper(content.split('\n'), separator)

    def readCSV(self):
        return self.readXSV(',')

    def readTSV(self):
        return self.readXSV('\t')

    def downloadBinary(self, file_name):
        content = self.readBinary()
        if content:
            File(file_name).writeBinary(content)

    @property
    def exists(self):
        try:
            response = requests.head(self.url, timeout=EXISTS_TIMEOUT)
            # pylint: disable=E1101
            return response.status_code == requests.codes.ok
        except requests.exceptions.ConnectTimeout:
            return False
