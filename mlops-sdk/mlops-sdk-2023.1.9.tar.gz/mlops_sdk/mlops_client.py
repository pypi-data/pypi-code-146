from typing import Any, Dict

from aiohttp import ClientSession, ClientTimeout, ContentTypeError, ServerTimeoutError
from asyncio import TimeoutError

from mlops_sdk.config import Config


class MlopsError(Exception):
    """
    Exception class for Mlops Client.
    """

    def __init__(self, code: int, msg: str, error_code: str = ""):
        super().__init__(msg)
        self.code = code
        self.msg = msg
        self.error_code = error_code


class MlopsClient:
    """
    Super class for clients.
    """

    def __init__(self, config: Config):
        self.config = config
        self.url = config.URL
        self.env = config.ENV
        self.apikey_header = {"x-api-key": config.APIKEY}

    async def _request(
        self,
        method: str,
        url: str,
        headers: Dict[str, Any] = None,
        data: Any = None,
        params=None,
        connection_timeout: float = 0.5,
        timeout: float = 1.5,
        retry: int = 1,
    ) -> Any:
        api_path = url
        async with ClientSession(timeout=ClientTimeout(total=timeout, connect=connection_timeout)) as session:
            for i in range(retry + 1):
                try:
                    async with session.request(
                        method=method,
                        url=f"{self.url}{'' if api_path.startswith('/') else '/'}{api_path}",
                        headers={**self.apikey_header, **headers} if headers else self.apikey_header,
                        json=data,
                        params=params,
                    ) as response:
                        try:
                            body = await response.json()
                            if not response.ok:
                                raise MlopsError(
                                    code=response.status,
                                    msg=self.apikey_header["x-api-key"] + " " + url + " " + body.get("message"),
                                    error_code=body.get("code"),
                                )
                            return body
                        except ContentTypeError:
                            return await response.text() or None
                except ServerTimeoutError:
                    if i == retry:
                        raise MlopsError(
                            code=500,
                            msg=f"Connection timeout occurred when requesting {self.url}{'' if api_path.startswith('/') else '/'}{api_path}",
                        )
                except TimeoutError:
                    if i == retry:
                        raise MlopsError(
                            code=500,
                            msg=f"Timeout occurred when requesting {self.url}{'' if api_path.startswith('/') else '/'}{api_path}",
                        )
