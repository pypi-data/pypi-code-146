import requests
from loguru import logger

from nood.api.responses import ResError, ResOK
from nood.config import API_DOMAIN
from nood.objects.product import Product


class Ping:
    def __init__(self, site_id: int, api_key: str):
        self.site_id = site_id
        self.api_key = api_key

    def products(self, *, products: list[Product]) -> bool:
        if not products:
            logger.debug("No products passed to ping")
            return False
        else:
            logger.debug(f"Pinging {len(products)} products")

        # update the products site id
        for p in products:
            p.site_id = self.site_id

        # send api request
        response = requests.post(
            url=f"{API_DOMAIN}/ping/product",
            headers={
                'Content-Type': 'application/json',
                'x-api-key': self.api_key
            },
            json={
                "products": [p.json() for p in products]
            }
        )

        # handle response
        if response.status_code == 200:
            res = ResOK(**response.json())
            logger.info(f"Successfully sent {len(products)} products to "
                        f"{res.number_of_webhooks}")
            return True
        elif response.status_code == 422:
            res = ResError(**response.json())
            logger.error(f"Error sending products: {res.message}")
            return False
        else:
            logger.error(f"Unknwon response: {response.status_code} "
                         f"'{response.text}'")
            return False
