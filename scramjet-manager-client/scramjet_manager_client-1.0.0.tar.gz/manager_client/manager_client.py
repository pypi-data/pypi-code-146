from client_utils import ClientUtils
from client.host_client import HostClient


class ManagerClient:
    def __init__(self, url: str, utils: ClientUtils = None):
        self.url = url
        self.client = utils or ClientUtils(url)
    
    async def get_host_client(self, id: str, host_api_base: str = '/api/v1'):
        return HostClient(self.url + '/sth/' + id + host_api_base)

    async def get_hosts(self) -> str:
        return await self.client.get('list')
    
    async def get_version(self) -> str:
        return await self.client.get('version')
    
    async def get_load(self) -> str:
        return await self.client.get('load')
    
    async def get_config(self) -> str:
        return await self.client.get('config')
    
    async def get_sequences(self) -> str:
        return await self.client.get('sequences')
    
    async def get_instances(self) -> str:
        return await self.client.get('instances')

    #TODO: to fix
    async def get_named_data(self, topic) -> str:
        return await self.client.get(f'topic/{topic}')
    
    async def get_log_stream(self) -> str:
        return await self.client.get('log')

    async def get_log(self) -> str:
        return await self.client.get_stream('log')
