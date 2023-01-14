from ..advanced import Request
from httpcore import Response
#from time import time

class Chats:
    def __init__(self, request: Request) -> None:
        self.request = request

    async def getChatsUpdates(self, state: str):
        data = {'state': state}
        response = self.request.Make(
            method='getChatsUpdates',
            data=data,
        )
        return await response