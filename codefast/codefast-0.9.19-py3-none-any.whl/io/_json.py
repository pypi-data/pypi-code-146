import ast
import base64
import gzip
import json
from typing import Any, Callable, Dict, List

import requests

from codefast.io.file import FileIO
from codefast.logger import error, info, warning


class Gzip(object):
    """Json 数据压缩与解压缩"""

    def compress(data: Dict) -> bytes:
        """ redis 返回 gzip 压缩后的数据可能会报无法解析的错误，
        所以外面又套了一层 base64。
        """
        json_data = json.dumps(data, indent=2)
        bytes = gzip.compress(json_data.encode('utf-8'))
        return base64.b64encode(bytes)

    def decompress(data: bytes) -> Dict:
        data = base64.b64decode(data)
        json_data = gzip.decompress(data).decode('utf-8')
        return json.loads(json_data)


class FastJson(object):

    def __call__(self, file_name: str = '') -> dict:
        if file_name:
            if file_name.startswith('http'):
                return requests.get(file_name).json()
            return self.read(file_name)

    def read(self, path_or_str: str) -> dict:
        ''' read from string or local file, return a dict'''
        if len(path_or_str) < 255:
            try:
                return json.loads(open(path_or_str, 'r').read())
            except FileNotFoundError as e:
                warning("input is not a file, {}".format(e))

        try:
            return ast.literal_eval(path_or_str)
        except SyntaxError as e:
            error("input is not a valid json string, {}".format(e))

        return {}

    def write(self, d: dict, file_name: str):
        json.dump(d, open(file_name, 'w'), ensure_ascii=False, indent=2)

    def eval(self, file_name: str) -> dict:
        '''Helpful parsing single quoted dict'''
        return ast.literal_eval(FileIO.read(file_name, ''))

    def dumps(self, _dict: dict) -> str:
        '''Helpful parsing single quoted dict'''
        return json.dumps(_dict)


class fpjson(object):
    """ functional programming json
    """

    def __init__(self, fpath: str = None) -> None:
        self.data = None
        if fpath:
            self.data = json.load(open(fpath, 'r'))

    def dump(self, file_name: str) -> 'fp.json':
        with open(file_name, 'w') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        return self

    def each(self, func: Callable) -> 'self':
        '''Helpful parsing single quoted dict'''
        if isinstance(self.data, dict):
            for k, v in self.data.items():
                self.data = func(k, v)
        elif isinstance(self.data, list):
            self.data = [func(e) for e in self.data]
        return self

    def filter(self, func: Callable) -> 'self':
        if isinstance(self.data, dict):
            self.data = {k: v for k, v in self.data.items() if func(k, v)}
        elif isinstance(self.data, list):
            self.data = [e for e in self.data if func(e)]
        return self

    def len(self) -> int:
        return len(self.data)

    def keys(self) -> List[Any]:
        return self.data.keys()

    def values(self) -> List[Any]:
        return self.data.values()

    def __repr__(self) -> str:
        return json.dumps(self.data, ensure_ascii=False, indent=2)

    def __setitem__(self, key, value):
        self.data[key] = value

    def __getitem__(self, key):
        return self.data[key]
