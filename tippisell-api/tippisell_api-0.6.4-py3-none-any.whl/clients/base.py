import http
import typing

from tippisell_api import methods, models, exceptions


class BaseClient:
    def __init__(self, shop_id: typing.Union[str, int], api_key: str):
        self.shop_id = str(shop_id)
        self.api_key = api_key

        self._base_url = "https://tippisell.xyz/api"

    async def get_user(self, user_id=None, telegram_id=None) -> models.User:
        raise NotImplementedError

    async def upload_goods(self, product_id: int, data: typing.List[str]) -> int:
        raise NotImplementedError

    async def _request(self, method: methods.BaseMethod):
        raise NotImplementedError

    def _http_request_kwargs(self, method: methods.BaseMethod) -> dict:
        if "get" == method.http_method:
            kwargs = {
                "params": method.get_params(),
            }
        elif method.http_method in ["post", "delete"]:
            kwargs = {"json": method.get_json()}
        else:
            raise NameError

        kwargs["method"] = method.http_method
        kwargs["headers"] = method.get_headers()
        kwargs["url"] = self._base_url + method.path
        return kwargs

    @classmethod
    def _check_response(cls, http_response: models.HttpResponse):
        if http.HTTPStatus.UNAUTHORIZED == http_response.status_code:
            raise exceptions.InvalidApiKey

        if http_response.result["ok"] is False:
            raise exceptions.BaseTippisellException(http_response.result["message"])
