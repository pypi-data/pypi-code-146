'''
HTTPS client to connect to any url:
Copyright 2022 Reyes Ruiz
https://github.com/Los-Vaqueros-Western-Wear/Scripts
'''

import sys
import base64
import requests
from com_digitalruiz_my_logger import my_logger

LOGGER = my_logger.set_logger(module_name=sys.argv[0], loglevel='INFO')

def get(url, headers=''):
    '''
    Simple http get method to grab data
    '''
    LOGGER.info("Getting %s", url)
    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code == 200:
        content = response.text
        return content
    LOGGER.error("Unable to get %s", url)
    return False

def get_image(url):
    '''
    Simple way to download jpg and convert it to base64
    '''
    LOGGER.info("Downloading image data %s", url)
    content = base64.b64encode(requests.get(url,timeout=60).content)
    return content

def post(url, headers='', data=''):
    '''
    Simple http post method
    '''
    LOGGER.info("posting to %s", url)
    response = requests.post(url, headers=headers, data=data, timeout=60)
    if response.status_code == 200:
        content = response.text
        return content
    LOGGER.error("Unable to post %s", url)
    return False

def get_cookies(url):
    '''
    Function to get cookies of a web url
    '''
    LOGGER.info("Getting %s", url)
    session = requests.Session()
    response = session.get(url)
    if response.status_code == 200:
        return session.cookies
    LOGGER.error("Unable to get %s", url)
    return False
