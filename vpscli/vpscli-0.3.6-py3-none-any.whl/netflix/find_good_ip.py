#!/usr/bin/env python
import subprocess
import time
from pprint import pprint

import codefast as cf
import requests


class Netflix:
    def __init__(self):
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML.36, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        self.test_url = 'https://www.netflix.com/title/81215567'
        self.proxies = {
            'http': 'socks5://127.0.0.1:23333',
            'https': 'socks5://127.0.0.1:23333'
        }

    def is_ip_supported(self):
        curl_ip = requests.get('https://ipinfo.io/json',
                               proxies=self.proxies).json()
        cf.info('current ipinfo is', curl_ip)
        resp = cf.net.get(self.test_url,
                          headers={'User-Agent': self.user_agent},
                          proxies=self.proxies)
        return resp.status_code == 200


class Warp:
    netflix = Netflix()

    def change_ip(self) -> bool:
        if self.netflix.is_ip_supported():
            cf.info(cf.fp.green('IP IS SUPPORTED!'))
            cf.info('current ipinfo is')
            pprint(
                requests.get('https://ipinfo.io/json',
                             proxies=self.netflix.proxies).json())
            return True
        cf.info(cf.fp.red('IP IS NOT SUPPORTED, CHANGING IP'))
        subprocess.call('warp-cli register; warp-cli connect;', shell=True)
        return False

    def run(self):
        for _ in range(3):
            if self.change_ip():
                break
            cf.info('trying in 5 seconds')
            time.sleep(5)


def entry():
    Warp().run()


if __name__ == '__main__':
    entry()
