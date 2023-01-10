import json
from manager_client.manager_client import ManagerClient
from client_utils import ClientUtils


class MultiManagerClient:
    def __init__(self, url: str, utils: ClientUtils = None):
        self.url = url
        self.client = utils or ClientUtils(url)
    
    async def get_manager_client(self, id: str, manager_api_base: str = '/api/v1'):
        return ManagerClient(self.url + '/space/' + id + manager_api_base)

    async def start_manager(self, config: dict, manager_api_base : str = '/api/v1'):
        resp = await self.client.post(
            url='start',
            headers={'content-type': 'application/json'},
            data=config
        )
        json_data = json.loads(resp)
        if 'error' in json_data:
            raise Exception(json_data.get('error'))
        return ManagerClient(self.url + '/space/' + json_data.get('id') + manager_api_base)

    async def get_managers(self) -> str:
        return await self.client.get('list')
    
    async def get_version(self) -> str:
        return await self.client.get('version')
    
    async def get_load(self) -> str:
        return await self.client.get('load')
    
    async def get_log_stream(self) -> str:
        return await self.client.get('log')
    
    async def get_info(self) -> str:
        return await self.client.get('info')