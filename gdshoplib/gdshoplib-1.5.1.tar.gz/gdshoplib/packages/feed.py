import datetime

from lxml import etree, objectify

from gdshoplib.core.settings import FeedSettings


class Feed:
    DESCRIPTION_TEMPLATE = "basic.txt"

    def __init__(self):
        self.feed_settings = FeedSettings()
        self.root = self.get_root()

    def get_root(self):
        root = etree.Element("yml_catalog")
        objectify.deannotate(root, cleanup_namespaces=True, xsi_nil=True)
        root.attrib["date"] = str(datetime.datetime.now())
        return root

    def get_shop(self):
        shop = objectify.Element("shop")

        shop.name = self.feed_settings.SHOP_NAME
        shop.company = self.feed_settings.COMPANY_NAME
        shop.url = self.feed_settings.SHOP_URL
        currencies = objectify.Element("currencies")
        currency = etree.Element("currency")
        currency.attrib["id"] = "RUB"
        currency.attrib["rate"] = "1"
        objectify.deannotate(currency, cleanup_namespaces=True, xsi_nil=True)
        objectify.deannotate(currencies, cleanup_namespaces=True, xsi_nil=True)
        currencies.append(currency)
        shop.currencies = currencies
        objectify.deannotate(shop, cleanup_namespaces=True, xsi_nil=True)

        return shop

    def get_offers(self, products):
        offers = etree.Element("offers")
        objectify.deannotate(offers, cleanup_namespaces=True, xsi_nil=True)
        for product in products:
            offers.append(self.get_offer(product))

        return offers

    @classmethod
    def get_old_price(cls, product):
        if (
            product.price.now <= product.price.profit / 1.05
        ):  # Старую цену можно указывать, только если разница больше 5%
            return product.price.profit

    def get_offer(self, product):
        appt = objectify.Element("offer")
        appt.attrib["id"] = product.sku
        appt.attrib["available"] = str(product.available()).lower()
        appt.currencyId = "RUB"
        appt.price = product.price.now
        appt.title = product.name
        appt.name = product.name
        appt.vendor = product.brand.title
        appt.delivery = "true"
        appt.description = product.description.generate(self)

        if self.get_old_price(product):
            appt.oldprice = self.get_old_price(product)

        for image in product.images:
            appt.addattr("picture", image.get_url())

        objectify.deannotate(appt, cleanup_namespaces=True, xsi_nil=True)
        return appt

    def get_feed(self, products):
        shop = self.get_shop()
        shop.append(self.get_offers(products))
        self.root.append(shop)
        return etree.tostring(
            self.root,
            pretty_print=True,
            encoding="utf-8",
            xml_declaration=True,
            standalone=True,
        )
