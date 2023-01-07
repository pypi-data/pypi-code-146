'''对nonebot的接受数据进行采样'''
from nonebot.adapters.onebot.v11.adapter import Adapter

# money patch
recv = Adapter.json_to_event
@classmethod
def json_to_event(cls, json_data: dict):
    return recv(json_data)
Adapter.json_to_event = json_to_event

# money patch
send = Adapter._call_api
async def _call_api(self, bot, api, **data):
    return await send(self, bot, api, **data)
Adapter._call_api = _call_api
