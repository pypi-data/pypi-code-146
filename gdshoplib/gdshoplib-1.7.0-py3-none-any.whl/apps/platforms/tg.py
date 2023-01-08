from gdshoplib.apps.platforms.base import BasePlatformManager
from gdshoplib.packages.feed import Feed


class TgManager(BasePlatformManager, Feed):
    KEY = "TG"
