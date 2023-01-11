import typing
import contextlib


class BaseMethod:
    http_method: typing.Literal["get", "post", "put", "delete"] = None
    path: str = None
    params: list = None
    json: list = None

    def __init__(self, **kwargs):
        self.kwargs = kwargs

        self._api_key = None

    def attach_api_key(self, api_key: str):
        self._api_key = api_key
        return self

    def attach_shop_id(self, shop_id: int):
        self.kwargs["shop_id"] = shop_id
        return self

    def get_params(self) -> dict:
        params = {}

        for key in self.params or []:
            with contextlib.suppress(KeyError):
                value = self.kwargs.get(key)
                if value is not None:
                    params[key] = value

        return params

    def get_json(self) -> dict:
        json_ = {}

        for key in self.json or []:
            with contextlib.suppress(KeyError):
                value = self.kwargs.get(key)
                if value is not None:
                    json_[key] = value

        return json_

    def get_headers(self) -> dict:
        return {"api-key": self._api_key}

    def validate(self):
        pass


class GetUser(BaseMethod):
    http_method = "get"
    path = "/v2/user/"
    params = ["user_id", "telegram_id", "shop_id"]

    def validate(self):
        assert 1 < len(self.get_params())


class UploadGoods(BaseMethod):
    http_method = "post"
    path = "/v2/product/upload"
    json = ["product_id", "data", "shop_id"]


class GetPurchases(BaseMethod):
    http_method = "get"
    path = "/v2/purchase/all"
    params = ["user_id", "shop_id", "limit"]


class GetShop(BaseMethod):
    http_method = "get"
    path = "/v2/shop"
    params = ["shop_id"]


class GetProducts(BaseMethod):
    http_method = "get"
    path = "/v2/product/all"
    params = ["offset", "limit", "order", "direction", "search", "shop_id"]


class CreateProduct(BaseMethod):
    http_method = "post"
    path = "/v2/product"
    json = [
        "name",
        "description",
        "type",
        "price",
        "category_id",
        "min_buy",
        "max_buy",
        "message_after_byu",
        "is_infinitely",
        "shop_id",
    ]


class DeleteProduct(BaseMethod):
    http_method = "delete"
    path = "/v2/product"
    json = ["id", "shop_id"]


class GetCountPositionsInProduct(BaseMethod):
    http_method = "get"
    path = "/v2/product/count-positions"
    params = ["product_id", "shop_id"]
