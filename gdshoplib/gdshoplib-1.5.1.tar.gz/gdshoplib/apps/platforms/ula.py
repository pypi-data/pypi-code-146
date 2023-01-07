from lxml import objectify

from gdshoplib.apps.platforms.base import BasePlatformManager
from gdshoplib.packages.feed import Feed


class UlaManager(BasePlatformManager, Feed):
    DESCRIPTION_TEMPLATE = "ula.txt"
    KEY = "ULA"

    def get_shop(self):
        shop = objectify.Element("shop")
        objectify.deannotate(shop, cleanup_namespaces=True, xsi_nil=True)

        return shop

    def get_offer(self, product):
        offer = super(UlaManager, self).get_offer(product)
        offer.youlaCategoryId = self.feed_settings.ULA_CATEGORY_ID
        offer.youlaSubcategoryId = self.feed_settings.ULA_SUBCATEGORY_ID
        offer.tovary_vid_zhivotnogo = 10463
        offer.managerName = self.feed_settings.MANAGER_NAME
        offer.address = self.feed_settings.ADDRESS
        offer.phone = self.feed_settings.PHONE
        objectify.deannotate(offer, cleanup_namespaces=True, xsi_nil=True)
        return offer
