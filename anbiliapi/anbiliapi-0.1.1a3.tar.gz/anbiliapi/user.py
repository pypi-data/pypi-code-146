import asyncio
from .utils import Bilibili


class User(Bilibili):

    async def get_user_info(self, mid: str = None) -> dict:
        """获取用户信息

        Args:
            mid (str, optional): 用户id,默认DedeUserID

        Returns:
            dict: _description_
        """
        mid = self._mid if mid is None else mid
        kwargs = {
            "url": "https://api.bilibili.com/x/space/acc/info",
            "method": "GET",
            "params": {"mid": mid},
        }
        res = await self._requests(**kwargs)
        return res.json()

    async def get_followings(self, mid: str = None, pn: int = 1, ps=50) -> dict:
        """获取关注列表
        别人只能获取前5页，自己可以获取所有
        Args:
            mid (str, optional): _description_. Defaults to None.
            pn (int, optional): _description_. Defaults to 1.
            ps (int, optional): _description_. Defaults to 50.

        Returns:
            dict: _description_
        """
        mid = self._mid if mid is None else mid
        kwargs = {
            "url": "https://api.bilibili.com/x/relation/followings",
            "method": "GET",
            "params": {"vmid": mid, "pn": pn, "ps": ps},
        }
        res = await self._requests(**kwargs)
        return res.json()

    async def get_all_followings(self, mid: str = None, waittime: int = 0) -> list:
        """
        获取自己所有的关注
        :param mid: 用户id
        :param waittime: 等待时间，防止过快412
        :return:
        """
        mid = self._mid if mid is None else mid
        followings_list = []
        pn = 0
        while True:
            pn += 1
            res = await self.get_followings(mid, pn)
            await asyncio.sleep(waittime)
            if not res.get("data", {}).get("list", []):
                break
            else:
                followings_list += res.get("data", {}).get("list", [])
        return followings_list

    async def user_concern(self, fid: int, is_concern: bool = True)->dict:
        """
        改变关注状态
        :param fid:用户id
        :param is_concern:是否关注
        :return:
        """
        kwargs = {
            "url": "https://api.bilibili.com/x/relation/modify",
            "method": "POST",
            "data": {"fid": fid, "act": 1 if is_concern else 2, "csrf": self._csrf},
        }
        res = await self._requests(**kwargs)
        return res.json()

    async def user_block(self, fid: int, is_block: bool = True)->dict:
        """
        改变黑名单状态
        :param fid:
        :param is_block:
        :return:
        """
        kwargs = {
            "url": "https://api.bilibili.com/x/relation/modify",
            "method": "POST",
            "data": {"fid": fid, "act": 5 if is_block else 6, "csrf": self._credential.bili_jct},
        }
        res = await self._requests(**kwargs)
        return res.json()

    async def get_video_release_list(self, mid: str = None, pn=1, ps=50) -> dict:
        mid = self._mid if mid is None else mid
        kwargs = {
            "url": "https://api.bilibili.com/x/space/arc/search",
            "method": "GET",
            "params": {"mid": mid, "pn": pn, "ps": ps}
        }
        res = await self._requests(**kwargs)
        return res.json()

    async def get_dynamic_list(self, mid: str = None,
                               offset: str = None, timezone_offset: int = -480) -> dict:
        mid = self._mid if mid is None else mid
        kwargs = {
            "url": "https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space",
            "method": "GET",
            "params": {"offset": offset, "host_mid": mid, "timezone_offset": timezone_offset}
        }
        res = await self._requests(**kwargs)
        return res.json()

    async def get_card_info(self, mid: str = None, photo: bool = False)->dict:
        mid = self._mid if mid is None else mid
        kwargs = {
            "url": "https://api.bilibili.com/x/web-interface/card",
            "method": "GET",
            "params": {"mid": mid, "photo": photo},
        }
        res = await self._requests(**kwargs)
        return res.json()
