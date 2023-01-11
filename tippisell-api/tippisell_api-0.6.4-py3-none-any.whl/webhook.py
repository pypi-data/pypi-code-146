import typing
from aiohttp import web

from tippisell_api import models


class WebhookRequestHandler(web.View):
    async def post(self):
        self.validate_ip()

        data = await self.request.json()

        response_data = {}
        if "pre_sell" == data["type"]:
            response_data["result"] = await self.validate_sale(
                models.User(**data["user"]),
                models.Product(**data["product"]),
                data["data"],
            )

        return web.json_response(response_data)

    async def validate_sale(
        self, user: models.User, product: models.Product, data: typing.List[str]
    ) -> typing.List[dict]:
        raise NotImplementedError

    def check_ip(self) -> bool:
        return "45.147.0.56" == self.request.headers.get("X-Forwarded-For")

    def validate_ip(self):
        if self.request.app.get("_check_ip", False):
            if self.check_ip() is False:
                raise web.HTTPUnauthorized()
