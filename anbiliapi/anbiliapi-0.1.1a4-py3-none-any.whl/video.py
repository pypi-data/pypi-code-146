from .utils import Bilibili, Credential, requests


async def get_video_info(aid: int = None, bvid: str = None):
    """
    获取视频信息
    :return:
    """
    kwargs = {
        "url": "https://api.bilibili.com/x/web-interface/view",
        "method": "GET",
        "params": {"aid": aid} if bvid is None else {"bvid": bvid}
    }
    res = await requests(**kwargs)
    return res.json()


class Video(Bilibili):
    def __init__(self, credential: Credential, aid: int = None, bid: str = None, proxies=None) -> None:
        super().__init__(credential, proxies)
        self._aid = aid
        self._bid = bid
        self._id = {"aid": aid} if bid is None else {"bvid": bid}

    async def get_video_info(self) -> dict:
        """
        获取视频信息
        :return:
        """
        kwargs = {
            "url": "https://api.bilibili.com/x/web-interface/view",
            "method": "GET",
            "params": self._id
        }
        res = await self._requests(**kwargs)
        return res.json()

    async def like(self, like: bool = True) -> dict:
        """
        点赞
        :param like:
        :return:
        """
        data = {"like": 1 if like else 2, "csrf": self._csrf}
        data.update(self._id)
        kwargs = {
            "url": "https://api.bilibili.com/x/web-interface/archive/like",
            "method": "POST",
            "data": data
        }
        res = await self._requests(**kwargs)
        return res.json()

    async def coin(self, multiply: int = 1, select_like: bool = True) -> dict:
        """
        投币
        :param select_like:
        :param multiply:
        :return:
        """
        data = {"multiply": 2 if multiply != 1 else 1, "csrf": self._csrf, "select_like": 1 if select_like else 0}
        data.update(self._id)
        kwargs = {
            "url": "https://api.bilibili.com/x/web-interface/coin/add",
            "method": "POST",
            "data": data
        }
        res = await self._requests(**kwargs)
        return res.json()
