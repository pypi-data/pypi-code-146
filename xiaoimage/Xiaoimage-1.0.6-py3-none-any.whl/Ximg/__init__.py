from bs4 import BeautifulSoup
import requests
import os
import urllib.request
import time
import sys
from bs import get_links, html_load, get_music

headers = {
    "Cookie": "UM_distinctid=16685e0279d3e0-06f34603dfa898-36664c08-1fa400-16685e0279e133; bdshare_firstime=1539844405694; gsScrollPos-1702681410=; CNZZDATA1254092508=1744643453-1539842703-%7C1539929860; _d_id=0ba0365838c8f6569af46a1e638d05",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
}
path = "./"
def load(url, path = './Ximg-download/'):
    get_links(url, path)
class html:
    def load_html(url, ob = 'html_download.html'):
        html_load(url, ob)
class music:
    def g_music(name, platfrom, index):
        get_music(name, platfrom, index)
def main():
    try:
        url = sys.argv[1]
        print('------getting url------')
        get_links(url)
    except Exception as e:
        print('Error: {}'.format(e))
        sys.exit(0)
