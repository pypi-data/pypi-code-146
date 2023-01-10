import random
import httpx
from httpx import ConnectError, ConnectTimeout, ProxyError, ReadTimeout, ReadError, UnsupportedProtocol
from scan.response import Response
from scan.common import logger


class Downloader(object):
    def __init__(self):
        self.client = None

    @staticmethod
    async def gen_headers():
        kit = f'{random.randint(490,540)}.{random.randint(10,90)}'
        return {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;'
                      'q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en;q=0.9',
            'user-agent': f'Mozilla/5.0 (Macintosh; Intel Mac OS X {random.randint(6,15)}_{random.randint(2,20)}'
                          f'_{random.randint(1,9)}) AppleWebKit/{kit} (KHTML, like Gecko) '
                          f'Chrome/{random.randint(95, 98)}.0.{random.randint(1000,5000)}.{random.randint(100, 200)}'
                          f' Safari/{kit}'
        }

    async def close(self):
        try:
            await self.client.aclose()
        except:
            pass

    @staticmethod
    async def log_request(request):
        pass

    @staticmethod
    async def log_response(response):
        """
        日志钩子
        """
        request = response.request
        if response.status_code not in [200, 301, 302]:
            logger.error(f'{response.status_code}  {request.url}')
        else:
            logger.info(f'{response.status_code}  {request.url}')

    async def request(self, url, params=None, headers=None, cookies=None, auth=None, proxies=None, allow_redirects=True,
                      verify=True, http2=False,  content=None, data=None, files=None, json=None, stream=False,
                      timeout=30, cycle=3):
        if data or json or content:
            method = 'POST'
        else:
            method = 'GET'
        if not headers:
            headers = await self.gen_headers()
        response = Response()
        response.request_url = url
        for _ in range(cycle):
            try:
                if stream:
                    client = httpx.AsyncClient(proxies=proxies, event_hooks={'response': [self.log_response]},
                                               verify=verify, http2=http2, follow_redirects=allow_redirects)
                    request = client.build_request(method=method, url=url, headers=headers, cookies=cookies,
                                                   content=content, data=data, files=files, json=json, timeout=timeout)
                    resp = await client.send(request, stream=True)
                    response.response = resp
                    response.ok = True
                    response.client = client  # need aclose
                else:
                    async with httpx.AsyncClient(proxies=proxies, event_hooks={'response': [self.log_response]},
                                                 verify=verify, http2=http2) as client:
                        resp = await client.request(
                            method=method, url=url, content=content, data=data, files=files, json=json, params=params,
                            headers=headers, cookies=cookies, auth=auth, follow_redirects=allow_redirects,
                            timeout=timeout
                        )
                        response.response = resp
                        response.ok = True
                return response
            except ConnectError as e:
                response.message = 'ConnectError'
                logger.error(f'Failed to request {url}  ConnectError:{e}')
            except ConnectTimeout as e:
                response.message = 'ConnectTimeout'
                logger.error(f'Failed to request {url}  ConnectTimeout:{e}')
            except ProxyError as e:
                response.message = 'ProxyError'
                logger.error(f'Failed to request {url}  ProxyError:{e}')
            except ReadTimeout as e:
                response.message = 'ReadTimeout'
                logger.error(f'Failed to request {url}  ReadTimeout:{e}')
            except ReadError as e:
                response.message = 'ReadError'
                logger.error(f'Failed to request {url}  ReadError:{e}')
            except UnsupportedProtocol as e:
                response.message = 'UnsupportedProtocol'
                logger.error(f'Failed to request {url}  UnsupportedProtocol:{e}')
            except Exception as e:
                response.message = e
                logger.error(f'Failed to request {url}  {e}')
        return response




