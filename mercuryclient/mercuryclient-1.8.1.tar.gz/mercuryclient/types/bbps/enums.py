from enum import Enum


class ShopType(Enum):

    KIRANA_SHOP = "KIRANA_SHOP"
    MOBILE_SHOP = "MOBILE_SHOP"
    COPIER_SHOP = "COPIER_SHOP"
    INTERNET_CAFE = "INTERNET_CAFE"
    OTHER = "OTHER"


class ComplaintType(Enum):
    Transaction = "Transaction"
    Service = "Service"
