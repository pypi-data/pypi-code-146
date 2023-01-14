from ..methods import Request, Chats
from ..methods import Chats
from typing import Optional
from time import time

class Client:
    def __init__(self, app_name: str, auth: Optional[str] = None, phone_number: Optional[str] = None) -> None:
        #self.__auth = auth
        request = Request(auth)
        self.Chats = Chats(request)

    async def getChatsUpdates(self, state: Optional[str] = str(round(time()) - 250)):
        res = await self.Chats.getChatsUpdates(state)
        return res.get('chats')