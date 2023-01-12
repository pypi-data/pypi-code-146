import os
from pathlib import Path
from typing import Optional

from pydantic import BaseSettings, DirectoryPath

BASEPATH = Path(os.path.dirname(os.path.realpath(__file__))).parent


class GeneralSettings(BaseSettings):
    TEMPLATES_PATH: DirectoryPath = (BASEPATH / "templates").resolve()
    MONTH_SALE_RATE: int = 9
    TURNOVER_RATE: int = 5


class NotionSettings(BaseSettings):
    NOTION_SECRET_TOKEN: str
    CACHE_ENABLED: bool = True


class FeedSettings(BaseSettings):
    PHONE: str = "+7 499 384 44 03"
    ADDRESS: str = "Москва, ул. Крупской, 4к1"
    MANAGER_NAME: str = "Менеджер магазина"
    SHOP_NAME: str = "Grey Dream Horse Shop (Конный магазин)"
    COMPANY_NAME: str = "GD Horse Shop (Конный магазин)"
    SHOP_URL: str = "https://www.instagram.com/gd_horse_shop/"
    ULA_CATEGORY_ID: int = 5
    ULA_SUBCATEGORY_ID: int = 507
    AVITO_CATEGORY: str = "Товары для животных"


class S3Settings(BaseSettings):
    ENDPOINT_URL: str = "https://storage.yandexcloud.net"
    BUCKET_NAME: str = "gdshop"
    ACCESS_KEY: str
    SECRET_KEY: str


class CacheSettings(BaseSettings):
    CACHE_CLASS: str = "KeyDBCache"
    CACHE_DSN: Optional[str]
    CACHE_HSTORE: str = "notion"
    CACHE_SYSTEM_HSTORE: str = "gdshoplib"


class ProductSettings(BaseSettings):
    PRODUCT_DB: str = "2d1707fb-877d-4d83-8ae6-3c3d00ff5091"


class PriceSettins(BaseSettings):
    # Базовые коэфиценты цены
    PRICE_VAT_RATIO: float = 0.16
    PRICE_NEITRAL_RATIO: float = 0.40
    PRICE_PROFIT_RATIO: float = 0.60
    EURO_PRICE: int = 72


class RecurrentCommonExpenseSettings(BaseSettings):
    # Общие месячные расходы
    CLOUD_HOSTING_MONTH: int = 2400
    PLATFORMS_MONTH: int = 2000
    AD_MONTH: int = 3000  # Рассход на общие рекламные компании

    def all(self):
        return sum([self.CLOUD_HOSTING_MONTH, self.PLATFORMS_MONTH, self.AD_MONTH])


class RecurrentSKUExpenseSettings(BaseSettings):
    # Расходы на каждую товарную позицию
    AVITO_SKU_PRICE: int = (
        2495 / 83
    )  # (общее количество затрат на просмотры в месяц) / (количество товаров)
    ULA_SKU_PRICE: int = 20
    PACKING_PRICE: int = 20

    def all(self):
        return sum([self.AVITO_SKU_PRICE, self.ULA_SKU_PRICE])


class OnceSKUExpenseSettings(BaseSettings):
    # Разовые расходы на каждый SKU
    DESCRIPTION_PRICE: int = 125

    def all(self):
        return sum([self.DESCRIPTION_PRICE])


class OnceProductExpenseSettings(BaseSettings):
    # Разовые расходы на каждый товар
    STOCK_DELIVERY_PRICE: int = 200 / 20

    def all(self):
        return sum([self.STOCK_DELIVERY_PRICE])


class VKSettings(BaseSettings):
    VK_BASEPATH: str = "https://api.vk.com/method/"
    VK_API_VERSION: str = "5.131"
    VK_GROUP_ID: str = "215870481"
    VK_CLIENT_ID: str = "51521300"
    VK_USER_SCOPE: str = "notify,friends,photos,audio,video,stories,pages,status,notes,wall,ads,offline,docs,groups,notifications,stats,email,market"
    VK_SECRET_KEY: Optional[str]
    VK_USER_ACCESS_TOKEN: Optional[str]


class AVITOSettings(BaseSettings):
    AVITO_CLIENT_ID: str = "PjsDDbv2OD294pmW1aak"
    AVITO_SECRET: str
