from gdshoplib.apps.platforms.base import Platform
from gdshoplib.packages.feed import Feed


class VkManager(Platform, Feed):
    DESCRIPTION_TEMPLATE = "vk.txt"
    KEY = "VK"
