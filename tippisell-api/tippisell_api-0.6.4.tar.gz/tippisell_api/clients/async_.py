import typing
import aiohttp

from . import base
from tippisell_api import methods, models


class Client(base.BaseClient):
    async def get_user(self, user_id=None, telegram_id=None) -> models.User:
        result = await self._request(
            methods.GetUser(user_id=user_id, telegram_id=telegram_id)
        )
        return models.User(**result)

    async def upload_goods(self, product_id: int, data: typing.List[str]) -> int:
        result = await self._request(
            methods.UploadGoods(product_id=product_id, data=data)
        )
        return result["count"]

    async def get_purchases(
        self, user_id: typing.Optional[typing.Union[str, int]] = None, limit=None
    ):
        result = await self._request(
            methods.GetPurchases(user_id=str(user_id), limit=limit)
        )
        return result

    async def get_shop(self) -> models.Shop:
        result = await self._request(methods.GetShop(shop_id=self.shop_id))
        return models.Shop(**result)

    async def get_products(
        self, offset: typing.Optional[int] = None, limit: typing.Optional[int] = None
    ) -> dict:
        result = await self._request(
            methods.GetProducts(shop_id=self.shop_id, offset=offset, limit=limit)
        )
        return result

    async def create_product(
        self,
        name: str,
        description: str,
        product_type: typing.Literal["text", "file"],
        price: float,
        category_id: typing.Optional[int] = None,
        min_buy: typing.Optional[int] = 1,
        max_buy: typing.Optional[int] = 9999,
        message_after_byu: typing.Optional[str] = None,
        is_infinitely: bool = False,
    ) -> dict:
        result = await self._request(
            methods.CreateProduct(
                shop_id=self.shop_id,
                name=name,
                description=description,
                type=product_type,
                price=price,
                category_id=category_id,
                min_buy=min_buy,
                max_buy=max_buy,
                message_after_byu=message_after_byu,
                is_infinitely=is_infinitely,
            )
        )
        return result

    async def delete_product(self, product_id: int):
        await self._request(methods.DeleteProduct(id=product_id))

    async def get_count_positions_in_product(self, product_id: int) -> int:
        result = await self._request(
            methods.GetCountPositionsInProduct(product_id=product_id)
        )
        return result["count"]

    async def _request(self, method: methods.BaseMethod):
        method.attach_shop_id(self.shop_id)
        method.attach_api_key(self.api_key)
        method.validate()

        async with aiohttp.ClientSession() as session:
            data = self._http_request_kwargs(method)
            response = await session.request(**data)
            await response.read()

        result = await response.json()
        self._check_response(
            models.HttpResponse(status_code=response.status, result=result)
        )

        return result["result"]
