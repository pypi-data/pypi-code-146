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
                return None
            return resp.content
        except requests.exceptions.ConnectionError:
            return None

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


def _read_helper(url, cached=True):
    warn(PendingDeprecationWarning)
    if cached:
        return _read_helper_cached(url)
    return _read_helper_nocached(url)


@cache('utils.www', timex.SECONDS_IN.HOUR)
def _read_helper_cached(url):
    warn(PendingDeprecationWarning)
    return _read_helper_nocached(url)


def _read_helper_nocached(url):
    warn(PendingDeprecationWarning)
    try:
        resp = requests.get(url, headers={'user-agent': USER_AGENT})
        if resp.status_code != 200:
            return None
        return resp.content
    except requests.exceptions.ConnectionError:
        return None


def _read_helper_selenium(url, cached=True):
    warn(PendingDeprecationWarning)
    if cached:
        return _read_helper_selenium_cached(url)
    return _read_helper_selenium_noncached(url)


@cache('utils.www', timex.SECONDS_IN.HOUR)
def _read_helper_selenium_cached(url):
    warn(PendingDeprecationWarning)
    return _read_helper_selenium_noncached(url)


def _read_helper_selenium_noncached(url):
    warn(PendingDeprecationWarning)
    browser = Browser(url)
    for _ in range(0, SELENIUM_SCROLL_REPEATS):
        browser.scroll_to_bottom()
        time.sleep(SELENIUM_SCROLL_WAIT_TIME)
    content = browser.get_source()
    browser.quit()
    return content


def read(url, cached=True, use_selenium=False):
    warn(PendingDeprecationWarning)
    """Read url."""
    if use_selenium:
        return _read_helper_selenium(url, cached)
    content = _read_helper(url, cached)
    return content.decode(ENCODING) if content else None


def read_json(url, cached=True):
    warn(PendingDeprecationWarning)
    """Read JSON content from url."""
    content = read(url, cached)
    return json.loads(content) if content else None


def read_tsv(url, cached=True):
    warn(PendingDeprecationWarning)
    """Read TSV content from url."""
    csv_lines = read(url, cached).split('\n')
    return tsv._read_helper(csv_lines)


def download_binary(url, file_name, cached=True):
    warn(PendingDeprecationWarning)
    """Download binary."""
    content = _read_helper(url, cached)
    filex.write(file_name, content, 'wb')
    logging.debug('Wrote %dB from %s to %s', len(content), url, file_name)


def exists(url, timeout=1):
    warn(PendingDeprecationWarning)
    """Check if URL exists."""
    try:
        response = requests.head(url, timeout=timeout)
        # pylint: disable=E1101
        return response.status_code == requests.codes.ok
    except requests.exceptions.ConnectTimeout:
        return False


def get_all_urls(root_url, cached=True):
    warn(PendingDeprecationWarning)
    """Get all URLs linked to a webpage."""
    soup = BeautifulSoup(read(root_url, cached), 'html.parser')
    urls = list(
        map(
            lambda a_link: a_link['href'],
            soup.find_all('a', href=True),
        )
    )
    logging.debug('Found %d links on %s', len(urls), root_url)
    return urls
