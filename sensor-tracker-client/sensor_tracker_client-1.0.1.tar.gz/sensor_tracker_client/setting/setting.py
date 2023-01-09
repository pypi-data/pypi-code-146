import os
from urllib.parse import urlparse

from . import basic_setting as default_setting


class Setting(object):

    def __init__(self):
        for setting in dir(default_setting):
            if setting.isupper():
                if setting == "HOST" or setting == "DEBUG_HOST":
                    setattr(self, "_" + setting, getattr(default_setting, setting))
                else:
                    setattr(self, setting, getattr(default_setting, setting))

    @property
    def HOST_URL(self):
        if self.DEBUG:
            return self.DEBUG_HOST
        else:
            return self.HOST

    @property
    def DEBUG_HOST(self):
        return self._DEBUG_HOST

    @DEBUG_HOST.setter
    def DEBUG_HOST(self, url):
        if not url.endswith("/"):
            url = url + "/"
        self._DEBUG_HOST = url

    @property
    def HOST(self):
        if not self._HOST:
            env_url = os.getenv(self.ENVIRONMENT_URL_VARIABLE_NAME)
            if env_url:
                self.HOST = env_url
            else:
                raise ValueError("Please setup the HOST url before using the sensor tracker client. stc.HOST = \"bla\"")
        return self._HOST

    @HOST.setter
    def HOST(self, url):
        if not url.endswith("/"):
            url = url + "/"
        o = urlparse(url)
        if url.endswith("api/"):
            url = url[:-4]
        if o.netloc:
            self._HOST = url
        else:
            raise ValueError("Not a valid URL")
