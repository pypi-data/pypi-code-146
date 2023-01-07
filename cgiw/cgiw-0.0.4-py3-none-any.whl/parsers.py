from os import getenv 
from sys import stdin
from urllib.parse import parse_qs

from .schemas import QueryType, HeadersType


def parse_query() -> QueryType:
    return parse_qs(getenv('QUERY_STRING'))


def parse_headers() -> HeadersType:
    return {
        'Content-Type': getenv('CONTENT_TYPE', ''),
        'Content-Length': getenv('CONTENT_LENGTH', '')
    }


def parse_body(headers: HeadersType) -> str:
    if length := int(headers.get('Content-Length') or 0):
        return stdin.read(length)
    return ''
