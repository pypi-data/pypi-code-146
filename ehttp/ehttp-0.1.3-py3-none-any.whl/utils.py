"""Класс для доп функций, е относящихся к конкретным объектам."""
import re
import socket
import logging

from .constants import FRAME_SIZE


def _url_parse(url):
    length = len(url)
    data = bytearray()
    i = 0
    while i < length:
        if url[i] != '%':
            char_code = ord(url[i])
            i += 1

        else:
            char_code = int(url[i+1:i+3], 16)
            i += 3

        data.append(char_code)

    return data.decode('utf8')


def _get_cookies(cookie_header):
    res = {}
    if cookie_header:
        for cookie in cookie_header.split(";"):
            splited = cookie.split("=", 1)
            res[splited[0]] = splited[1]
    return res


def _get_headers(headers_data: bytes):
    result = {}
    for header in headers_data.decode().split("\r\n"):
        key = header.split(":", 1)[0].strip()
        value = header.split(":", 1)[1].strip()
        result[key.lower()] = value
    return result


def _set_headers(headers: dict):
    result = b""
    for key in headers.keys():
        result += f"{key}: {headers[key]}\r\n".encode()
    return result


def _get_data(sock: socket.socket):
    pdata = b""
    headers_data = b""
    data_len = -1
    try:
        while True:
            if headers_data:
                sock.settimeout(5)
            data = sock.recv(FRAME_SIZE)
            sock.settimeout(None)

            pdata += data
            if b"\r\n\r\n" in pdata and not headers_data:
                splited = pdata.split(b"\r\n\r\n", 1)
                headers_data = splited[0]
                data_len_raw = re.findall(rb"content-length: (\d+)", headers_data.lower())
                if data_len_raw:
                    data_len = int(data_len_raw[0])
                pdata = splited[1]
                if not pdata:
                    pdata = b"\r\n"

            if len(data) == 0:
                break

            if headers_data:
                if (pdata[-2:] == b"\r\n" and len(data) < FRAME_SIZE) or \
                        (len(pdata) == int(data_len)):  # EOF
                    break
    except TimeoutError:
        logging.warning("Timeout.")
    return (pdata, headers_data)
