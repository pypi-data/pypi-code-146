from manager_client.manager_client import ManagerClient
from client_utils.client_utils import ClientUtils


class MiddlewareClient:
    def __init__(self, url: str = None, utils: ClientUtils = None) -> None:
        self.api_base = url
        self.client = utils or ClientUtils(url)

    async def get_managers(self) -> str:
        return await self.client.get("spaces")

    async def get_version(self) -> str:
        return await self.client.get("version")

    async def get_manager_client(self, id: str, manager_api_base: str = "/api/v1"):
         return ManagerClient(self.api_base + '/space/' + id + manager_api_base)


