from gdshoplib.apps.platforms.base import BasePlatformManager
from gdshoplib.packages.feed import Feed


class OkManager(BasePlatformManager, Feed):
    KEY = "OK"
