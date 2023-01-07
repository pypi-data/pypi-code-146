import time
from random import randint
from .utils import Bilibili, requests, Credential


async def get_dynamic_list(mid: int, offset: str = None, timezone_offset: int = -480) -> dict:
    """
    获取动态列表
    :param mid:
    :param offset:
    :param timezone_offset:
    :return:
    """
    kwargs = {
        "url": "https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space",
        "method": "GET",
        "data": {"offset": offset, "host_mid": mid, "timezone_offset": timezone_offset}
    }
    res = await requests(**kwargs)
    return res.json()


async def lottery_notice(dynamic_id: int):
    """
    查看互动抽奖信息
    dynamic_id:
    :return:
    """

    kwargs = {
        "url": "https://api.vc.bilibili.com/lottery_svr/v1/lottery_svr/lottery_notice",
        "method": "GET",
        "params": {"dynamic_id": dynamic_id}
    }
    res = await requests(**kwargs)
    return res.json()


class Dynamic(Bilibili):

    def __init__(self, credential: Credential, did: int, proxies=None) -> None:
        super().__init__(credential, proxies=proxies)
        self.did = did
        self._dyn_id_str = {"dyn_id_str": str(did)}
        self._dynamic_id = {"dynamic_id": did}

    async def get_dynamic_list(self, mid: int = None, offset: str = None, timezone_offset: int = -480) -> dict:
        """
        获取动态列表
        :param mid:
        :param offset:
        :param timezone_offset:
        :return:
        """
        mid = self._mid if mid is None else mid
        kwargs = {
            "url": "https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space",
            "method": "GET",
            "params": {"offset": offset, "host_mid": mid, "timezone_offset": timezone_offset}
        }
        res = await self._requests(**kwargs)
        return res.json()

    async def remove(self, dyn_id_str: str = None):
        kwargs = {
            "url": f"https://api.bilibili.com/x/dynamic/feed/operate/remove?csrf={self._csrf}",
            "method": "POST",
            "json": self.__get_dyn_id_str(dyn_id_str)
        }
        res = await self._requests(**kwargs)
        return res.json()

    async def forward(self, raw_text: str = "转发动态", dyn_id_str: str = None):
        """分享动态

        Args:
            raw_text (str, optional): _description_. Defaults to "转发动态".

        Returns:
            _type_: _description_
            :param raw_text:
            :param dyn_id_str:
        """
        kwargs = {
            "url": f"https://api.bilibili.com/x/dynamic/feed/create/dyn?csrf=8e183b7b10560b878d21b4b9a9c425bc",
            "method": "POST",
            "json": {"dyn_req": {"content": {"contents": [{"raw_text": raw_text, "type": 1, "biz_id": ""}]}, "scene": 4,
                                 "upload_id": f"{self._mid}_{time.time()}_{randint(0, 10000)}",
                                 "meta": {"app_meta": {"from": "create.dynamic.web", "mobi_app": "web"}}},
                     "web_repost_src": self.__get_dyn_id_str(dyn_id_str)}
        }
        res = await self._requests(**kwargs)
        return res.json()

    async def lottery_notice(self, dynamic_id: int = None):
        """
        查看互动抽奖信息
        dynamic_id:
        :return:
        """

        kwargs = {
            "url": "https://api.vc.bilibili.com/lottery_svr/v1/lottery_svr/lottery_notice",
            "method": "GET",
            "params": self.__get_dynamic_id(dynamic_id)
        }
        res = await self._requests(**kwargs)
        return res.json()

    async def like(self, dynamic_id: int, like: bool = True, ):
        """
        动态点赞
        :param dynamic_id:
        :param like:
        :return:
        """
        kwargs = {
            "url": f"https://api.vc.bilibili.com/dynamic_like/v1/dynamic_like/thumb",
            "method": "POST",
            "data": {"dynamic_id": dynamic_id,
                     "up": 1 if like else 2,
                     "csrf": self._csrf
                     }
        }
        res = await self._requests(**kwargs)
        return res.json()

    def __get_dynamic_id(self, dynamic_id: int) -> dict:
        return self._dynamic_id if dynamic_id is None else {"dynamic_id": dynamic_id}

    def __get_dyn_id_str(self, dyn_id_str: str) -> dict:
        return self._dyn_id_str if dyn_id_str is None else {"dyn_id_str": dyn_id_str}
