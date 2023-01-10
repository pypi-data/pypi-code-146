from client_utils import ClientUtils


class HostClient:
    def __init__(self, url: str, utils: ClientUtils = None) -> None:
        self.url = url
        self.client = utils or ClientUtils(url)
 
    async def list_sequences(self) -> str:
        url = f'sequences'
        return await self.client.get(url)
    
    async def list_instances(self) -> str:
        url = f'instances'
        return await self.client.get(url)
        
    async def get_data(self, seq_path: str) -> bytes:
        with open(seq_path, 'rb') as f:
            return f.read()

    async def send_sequence(self, file, app_config = None) -> str:
        url = f'sequence'
        data = await self.get_data(file)
        return await self.client.post(url, data=data, config=app_config)

    async def get_sequence(self, id: str) -> str:
        return await self.client.get(f'sequence/{id}')

    async def delete_sequence(self, id: str) -> str:
        url = f'sequence/{id}'
        headers = {'Content-Type': 'application/json'}
        return await self.client.delete(url, headers=headers)

    async def get_instance_info(self, id: str) -> str:
        return await self.client.get(f'instance/{id}')

    async def get_load_check(self) -> str:
        return await self.client.get('load-check')

    async def get_version(self) -> str:
        return await self.client.get('version')
   
    async def get_log_stream(self) -> str:
        return await self.client.get('log')

    async def send_named_data(self, topic: str, stream: str, content_type: str, end: bool):
        data = {'type': content_type, 'end': end, 'parse_response': 'stream'}
        return await self.client.send_stream(f'topic/{topic}', stream, options=data)

    async def get_named_data(self, topic: str):
        return await self.client.get(f'topic/{topic}')
