from typing import List

from pydantic import BaseModel

from nood.objects.product import Product


class PingProductsBody(BaseModel):
    products: List[Product]
