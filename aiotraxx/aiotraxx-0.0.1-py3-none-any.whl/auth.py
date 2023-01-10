import os
import pathlib
from typing import AsyncGenerator, Optional

import toml
from aiohttp import ClientRequest, ClientResponse
from aiohttp.connector import Connection
from dints.util.aiohttp import AuthFlow



class TraxxAuthFlow(AuthFlow):
    def __init__(self, path: Optional[os.PathLike] = None) -> None:
        path = path or os.getenv("TRAXX_CLIENT_SESSION")
        if not path:
            raise ValueError(
                "No filepath specified for Traxx session cookies. You must enter "
                "a filepath or set the INSIGHT_SESSION_FILEPATH environment variable."
            )
        path = pathlib.Path(path)
        if not path.exists():
            raise FileNotFoundError(path.__str__())
        self._path = path

    async def auth_flow(
        self,
        request: ClientRequest,
        _: Connection
    ) -> AsyncGenerator[None, ClientResponse]:
        cookies = toml.loads(self._path.read_text())
        request.update_cookies(cookies)
        yield