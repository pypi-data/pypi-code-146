import functools

from .setting import setting
from .api_binder_factory import API_METHOD_INFO, make_api_methods
from .authentication import authentication
from .exceptions import AuthenticationError


@functools.lru_cache(maxsize=None)
def all_name():
    the_name_list = []
    for i in API_METHOD_INFO:
        the_name_list.append(i["keyword"])
    return the_name_list


class SensorTrackerClient:
    def __init__(self):
        make_api_methods(self, API_METHOD_INFO)

    @property
    def basic(self):
        return setting

    @basic.setter
    def basic(self, value):
        raise Exception("You can't not modified 'basic' attribute")

    @property
    def HOST(self):
        return self.basic.HOST

    @HOST.setter
    def HOST(self, value):
        self.basic.HOST = value

    @property
    def cache_on(self):
        return setting.CACHE_ON

    @cache_on.setter
    def cache_on(self, value):
        assert type(value) is bool, (
            "cache on can be assigned True or False "
        )
        setting.CACHE_ON = value

    @property
    def authentication(self):
        return authentication

    @authentication.setter
    def authentication(self, value):
        raise AuthenticationError("You can't not modified 'authentication' attribute")

    @property
    def setting(self):
        print("will be ready soon")
        return None

    @setting.setter
    def setting(self, value):
        res = {}
        raise AuthenticationError("You can't not modified 'setting' attribute")

    def __setattr__(self, key, value):
        if key in all_name() and hasattr(self, key):
            raise AuthenticationError("Can't change")
        super().__setattr__(key, value)
