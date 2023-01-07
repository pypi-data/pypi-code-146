from os import getenv 
from urllib.parse import parse_qs
from sys import stdin
from typing import Dict, Tuple, Union, List
from abc import abstractmethod


class Handler:
    def __init__(self, verbose=True):
        if verbose:
            print(self.run())

    def run(self):
        method = getenv('REQUEST_METHOD')
        query = self.parse_query()
        headers = self.parse_headers()
        body = self.parse_body(headers)
        response = self.handle(method, query, headers, body)
        return self.compose_response(*response)

    @staticmethod
    def parse_query() -> Dict[str, Union[str, List[str]]]:
        return {k: v if len(v) > 1 else v[0] for k, v in parse_qs(getenv('QUERY_STRING')).items()}

    @staticmethod
    def parse_headers() -> Dict[str, str]:
        return {
            'Content-Type': getenv('CONTENT_TYPE', ''),
            'Content-Length': getenv('CONTENT_LENGTH', '')
        }

    @staticmethod
    def parse_body(headers: Dict[str, str]) -> str:
        if length := int(headers.get('Content-Length') or 0):
            return stdin.read(length)
        return ''
    
    def handle(self, method, query, headers, body) -> Tuple[str, Dict[str, str], str]:
        response: Tuple[str, Dict[str, str], str] = ('200', {}, '')
        try:
            if method == 'POST':
                response = self.post(query, headers, body)
            elif method == 'GET':
                response = self.get(query, headers)
        except NotImplementedError:
            response = ('405 Method Not Allowed', {}, '')
        return response

    @staticmethod
    def compose_response(status, headers, body) -> str:
        formatted_headers = '\n'.join([f"{k}: {v}" for k, v in headers.items()])
        return f"Status: {status}\n{formatted_headers}\n\n{body}"

    @abstractmethod
    def get(self, query: Dict[str, Union[str, List[str]]], headers: Dict[str, str]) -> Tuple[str, Dict[str, str], str]:
        raise NotImplementedError()

    @abstractmethod
    def post(self, query: Dict[str, Union[str, List[str]]], headers: Dict[str, str], body: str) -> Tuple[str, Dict[str, str], str]:
        raise NotImplementedError()