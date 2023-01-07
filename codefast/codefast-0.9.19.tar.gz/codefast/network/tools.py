import os
from pathlib import Path

import requests
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from tqdm import tqdm

from codefast.io import FileIO
from codefast.io.file import FormatPrint, ProgressBar
from codefast.logger import get_logger
from codefast.network.factory import Spider


class Network(object):
    log = get_logger()
    spider = Spider().born()

    @classmethod
    def parse_headers(cls, str_headers: str) -> dict:
        lst = [u.split(':', 1) for u in str_headers.split('\n')]
        return dict((u[0].strip(), u[1].strip()) for u in lst)

    @classmethod
    def get(cls, url: str, **kwargs) -> requests.models.Response:
        return cls.spider.get(url, **kwargs)

    @classmethod
    def post(cls, url: str, **kwargs) -> requests.models.Response:
        return cls.spider.post(url, **kwargs)

    @staticmethod
    def upload_file(upload_url: str,
                    file_path: str,
                    **kargs) -> requests.Response:
        from tqdm.utils import CallbackIOWrapper
        file_size = os.stat(file_path).st_size
        resp = None
        with open(file_path, "rb") as f:
            with tqdm(total=file_size, unit="B", unit_scale=True, unit_divisor=1024) as t:
                wrapped_file = CallbackIOWrapper(t.update, f, "read")
                resp = requests.put(upload_url, data=wrapped_file, **kargs)
        return resp


    @classmethod
    def _resume(cls,
                url: str,
                name: str,
                resume_byte_pos: int = 0,
                proxies=None) -> None:
        resume_header = {'Range': 'bytes=%d-' % resume_byte_pos}
        if resume_byte_pos > 0:
            response = requests.get(url,
                                    stream=True,
                                    headers=resume_header,
                                    proxies=proxies)
            file_mode = 'ab'
        else:
            response = requests.get(url, stream=True, proxies=proxies)
            file_mode = 'wb'

        total_bytes = int(response.headers.get('content-length', 0))
        cls.log.info("remaining size: {}".format(FormatPrint.sizeof_fmt(total_bytes)))
        block_size, acc = 1024, 0  # 8 Kibibyte
        pb = ProgressBar()
        with open(name, file_mode) as f:
            for chunk in response.iter_content(block_size):
                pb.run(acc, total_bytes)
                acc += block_size
                f.write(chunk)
            pb.run(total_bytes, total_bytes)
        print('')
        cls.log.info("download completed.")

    @classmethod
    def download(cls, url: str, name=None, proxies=None) -> None:
        name = name or url.split('/').pop().strip()

        if not FileIO.exists(name):
            cls.log.info("start new download task {}".format(name))
            cls._resume(url, name, proxies=proxies)
        else:
            resume_bytes = os.path.getsize(name)
            total_bytes = int(
                requests.get(url, stream=True, proxies=proxies).headers.get(
                    'content-length', -1))
            event = {'resume_bytes': resume_bytes, 'total_bytes': total_bytes}
            cls.log.info(event)
            while total_bytes - resume_bytes > 8:
                cls.log.info({resume_bytes, total_bytes})
                cls.log.info('resume downloading {}'.format(name))
                try:
                    cls._resume(url, name, resume_bytes, proxies=proxies)
                except Exception as e:
                    cls.log.error(repr(e))
                resume_bytes = os.path.getsize(name)


def urljoin(*args):
    """Join args into a url. Trailing but not leading slashes are removed."""
    args = [str(x).rstrip('/').lstrip('/') for x in args]
    return '/'.join(args)


def url_shortener(url: str) -> str:
    # gg.gg url shortener
    host = 'https://ddot.fun/s'
    js = requests.post(host, json={'url': url}).json()
    return js['url']


def bitly(uri: str, printout: bool = True) -> str:
    if not uri.startswith('http'):
        uri = f'http://{uri}'
    # print(author.get('bitly_token'))
    token_file = Path(os.path.expanduser('~/.config/bitly_token'))
    if not token_file.exists():
        print('bitly token file not found')
        return uri
    bitly_token = token_file.read_text().strip()
    query_params = {'access_token': bitly_token, 'longUrl': uri}
    endpoint = 'https://api-ssl.bitly.com/v3/shorten'
    response = requests.get(endpoint, params=query_params)

    data = response.json()
    if printout:
        print(query_params)
        print("{:<20} {}".format("long url", uri))
        print("{:<20} {}".format("shorten url", data['data']['url']))
    return data['data']['url']
