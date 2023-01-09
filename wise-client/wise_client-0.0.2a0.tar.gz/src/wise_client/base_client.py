import httpx
from typing import Any, Union

BASE_URL = "https://api.transferwise.com"
SANDBOX_BASE_URL = "https://api.sandbox.transferwise.tech"


class BaseClient():

    def __init__(self, api_key: str, is_sandbox: bool = True,
                 lang: str = "en") -> None:
        """Initialise a client instance.

        Args:
          api_key: An api key obtained from your Wise account
          is_sandbox: Use the production endpoint if false, use the sandbox
          endpoint otherwise
          lang: Refer [here](https://api-docs.wise.com/#language-support) for
          supported value
        """
        self.is_sandbox = is_sandbox
        self.api_key = api_key
        self.http_client = httpx.AsyncClient(
                                headers={
                                    "Authorization": f"Bearer {self.api_key}",
                                    "Accept-Language": lang},
                                http2=True)

    def _construct_url(self, endpoint: str) -> str:
        endpoint = endpoint.rstrip("/")
        url = SANDBOX_BASE_URL if self.is_sandbox else BASE_URL
        url += endpoint
        return url

    async def disconnect(self) -> None:
        """Terminate HTTP connection. The instance will not be usable after
        this call.
        """
        if self.http_client is not None:
            await self.http_client.aclose()
            self.http_client = None

    async def query(self, method: str = "GET", endpoint: str = "/",
                    params: Union[httpx._types.QueryParamTypes, None] = None,
                    data: Union[Any, None] = None
                    ) -> Any:
        """Make a HTTP query to the specified endpoint at the base URL.

        Args:
          method: HTTP method for the query. Only accepts `GET` and `POST`.
          endpoint: The endpoint of the HTTP request.
          params: Parameters to be included in the URL
          data: Types that can be serialised into JSON to be included as
          payload in the request

        Returns:
          The de-serialised JSON respond from the server.

        Raises:
          HttpStatusError: If the HTTP response status code is not 2xx.
          NotImplementedError: Unknown or unimplemented HTTP method provided.
        """
        url = self._construct_url(endpoint)
        if method == "GET":
            result = await self.http_client.get(url=url, params=params)
        elif method == "POST":
            result = await self.http_client.post(url=url,
                                                 params=params,
                                                 json=data)
        else:
            raise NotImplementedError("HTTP method not implemented")
        result.raise_for_status()
        return result.json()
