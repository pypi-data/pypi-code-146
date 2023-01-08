from gdshoplib.apps.platforms.base import BasePlatformManager
from gdshoplib.packages.feed import Feed


class InstagramManager(BasePlatformManager, Feed):
    DESCRIPTION_TEMPLATE = "instagram.txt"
    KEY = "INSTAGRAM"
