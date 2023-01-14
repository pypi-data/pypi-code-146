import getopt
import re
import sys

import requests

from helpers.DriverManager import DriverManager
from bs4 import BeautifulSoup
import pandas as pandas
from helpers.common import Common
import speedboat
import wget
import ssl
from config import nRoboConfig


def start_selenium_grid(type="standalone"):
    # webdriver = DriverManager.get_browser("headless_chrome")

    url_base = "https://github.com"
    url_scrap = url_base + "/SeleniumHQ/selenium/releases"

    # Using webdriver
    # webdriver.get(url_scrap)

    # Using requests
    page_content = requests.get(url_scrap).text

    # Beautify Content
    soup = BeautifulSoup(page_content, 'html.parser')

    # for anchor_tag in soup.find_all("a", href=re.compile(r'.jar')):
    #     print(anchor_tag)

    # for anchor_tag in soup.find_all("a", href= lambda x: x and '.jar' in x):
    #     print(anchor_tag)

    for anchor_tag in soup.select('a[href*=\.jar]'):

        url_selenium_jar = url_base + anchor_tag['href']
        # print(url_selenium_jar)

        # Download selenium jar
        # response = requests.get(url_selenium_jar)
        # content_type = response.headers.get("content-type")
        # print(content_type)

        if url_selenium_jar.find('/'):
            download_file_name = url_selenium_jar.rsplit('/', 1)[1]
        print(download_file_name)

        if Common.is_file_exist(download_file_name):
            # Do nothing
            pass
        else:
            try:
                # Download
                ssl._create_default_https_context = ssl._create_stdlib_context
                response = wget.download(url_selenium_jar, download_file_name)
                print("{0}, downloaded successfully.", response)

            except Exception as e:
                print(e)

                speedboat.system_command("rm -f " + download_file_name)

        print("Starting Selenium Grid...")
        speedboat.system_command("java -jar " + download_file_name + " standalone")

        # No need to further download
        exit(1)


if __name__ == '__main__':

    # Check command line switch -t / Target Environment
    argv = sys.argv[1:]
    print(argv)

    # parse command line switches
    try:
        switches, arguments = getopt.getopt(argv, 't:h:n:p:', ["type", "hub", "node", "port"])

        print(switches)
        # print(arguments)

    except getopt.GetoptError as e:
        # Print error
        print(e)

    # Process command line switches
    for switch, value in switches:
        # print(switch + "=" + value)

        pass

    exit(1)

    # start_selenium_grid()
