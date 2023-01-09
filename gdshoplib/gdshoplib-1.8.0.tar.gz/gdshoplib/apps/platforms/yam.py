from gdshoplib.apps.platforms.base import BasePlatformManager
from gdshoplib.packages.feed import Feed


class YandexMarketManager(BasePlatformManager, Feed):
    KEY = "YM"
