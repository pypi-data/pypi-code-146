import base64
import os

import codefast as cf
from .meta import BASE64_URLS


class Piper:
    def get(self, app_name: str):
        url = base64.b64decode(BASE64_URLS[app_name]).decode('utf-8').rstrip()
        cf.info('downloading [{}] from [{}]'.format(app_name, url))
        cf.net.download(url, os.path.join('/tmp/', app_name))

    def put(self, app_name: str, data: str):
        raise NotImplementedError


class DependencyDownloader(object):
    def __init__(self):
        self.pp = Piper()

    def run(self):
        for app_name in BASE64_URLS:
            self.pp.get(app_name)
