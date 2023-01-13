from httpx import AsyncClient
from .err import ResponseCodeException, NetworkException
from .credential import Credential


async def requests(url: str,
                   method: str = "GET",
                   cookies: dict = None,
                   data: dict = None,
                   files=None,
                   json: dict = None,
                   params: dict = None,
                   proxies=None
                   ):
    cookies = {} if cookies is None else cookies
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.46"}
    client = AsyncClient(timeout=60, headers=headers, proxies=proxies)
    try:
        if method == "GET":
            req = client.get(url, params=params, cookies=cookies)
        else:
            req = client.post(url, data=data, cookies=cookies, files=files, json=json, params=params)
        res = await req
    finally:
        await client.aclose()

    if res.status_code != 200:
        raise NetworkException(res.status_code, res.text)

    return res


async def requests_json(url: str,
                        method: str = "GET",
                        cookies: dict = None,
                        data: dict = None,
                        files=None,
                        json: dict = None,
                        params: dict = None,
                        proxies=None) -> dict:
    res = await requests(url=url,
                         method=method,
                         cookies=cookies,
                         data=data,
                         files=files,
                         json=json,
                         params=params,
                         proxies=proxies)
    if res.json().get("code") != 0:
        raise ResponseCodeException(res.json().get("code"), res.json().get("message"), res.json())

    return res.json()


class Requests:

    def __init__(self, credential: Credential, proxies=None):
        self.__credential = credential
        self.__proxies = proxies

    async def requests(self,
                       url: str,
                       method: str = "GET",
                       cookies: dict = None,
                       data: dict = None,
                       files=None,
                       json: dict = None,
                       params: dict = None,
                       proxies=None
                       ):
        cookies = {} if cookies is None else cookies
        cookies.update(self.__credential.dict())
        return await requests(url=url,
                              method=method,
                              cookies=cookies,
                              data=data,
                              files=files,
                              json=json,
                              params=params,
                              proxies=proxies)

    async def requests_json(self,
                            url: str,
                            method: str = "GET",
                            cookies: dict = None,
                            data: dict = None,
                            files=None,
                            json: dict = None,
                            params: dict = None,
                            proxies=None
                            ) -> dict:
        cookies = {} if cookies is None else cookies
        cookies.update(self.__credential.dict())
        res = await requests_json(url=url,
                                  method=method,
                                  cookies=cookies,
                                  data=data,
                                  files=files,
                                  json=json,
                                  params=params,
                                  proxies=proxies)
        return res
