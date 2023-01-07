"""Базовые классы для работы с запросами."""
from __future__ import annotations
import re
import json
import socket
import logging
import datetime
import traceback
from typing import Optional

from .utils import _get_headers, _get_cookies, _set_headers, _url_parse
from .constants import CODES, DEFAULT_HEADERS, CORS_HEADERS, SERVER, TYPES


class File():
    """Класс для работы с получаемыми и отправляемыми сервером файлами."""
    @staticmethod
    def get(headers_data: bytes, data: bytes) -> list[File]:
        """Метод для получения файлов из сырого запроса.

        Args:
            headers_data (bytes): сырые заголовки
            data (bytes): сырые данные

        Returns:
            list: список файлов
        """

        res = []
        boundary = re.findall(rb"boundary=(?:-)+([^-|^\n]+)", headers_data)
        if boundary:
            reg = b"(?:-*"+boundary[0][:-1]+b"-*(?:\r\n)*)"
            files_data = re.split(reg, data)[1:-1]

            for file in files_data:
                keys = {}

                for file_variable in file.split(b"\n", 1)[0].split(b';'):
                    try:

                        keys[
                            file_variable.split(b"=", 1)[
                                0].decode().replace(" ", "")
                        ] = file_variable.split(
                            b"=", 1)[1].split(b'"')[1].decode()
                    except IndexError:
                        pass
                filename = keys.get("filename", '{{filename field}}')
                name = keys.get("name", '{{name field}}')
                data = file.split(b"\r\n\r\n", 1)[1]
                res.append(File(filename, name, data[:-2], keys))
        return res

    def __init__(self, filename: str, name=None, data=None, keys=None):
        """Файл. Отправляемый или получаемый.

        Args:
            filename (str): путь до файла
            name (str, optional): имя файла. Defaults to None
            data (bytes, optional): сырое содержимое файла. Defaults to None
            keys (dict, optional): ключи файла(входящие данные). Defaults to None
        """
        self.name = name
        "Имя файла(для входящих)"
        self.filename = filename
        "Путь до файла"
        self.data = data
        "Сырое содержимое файла"
        self.keys = keys or {}
        "Ключи файла(для входящих)"
        if not data:
            with open(filename, "rb") as file:
                self.data = file.read(-1)

    def __str__(self):
        return f"name={self.name}; filename={self.filename};\n{self.data}"


class Request():  # pylint: disable=too-many-instance-attributes,too-few-public-methods
    """Базовый класс для работы с входящими запросами."""

    def __init__(self, data: bytes, headers: bytes):
        """Входящий запрос.

        Args:
            data (bytes): сырые данные
            headers (bytes): сырые заголовки
        """
        first = re.findall(r"([^ ]+) ([^ ]+) ([^\r]+)", headers.decode())[0]
        self.method = first[0]
        "HTTP метод"
        self.raw_path = first[1]
        "Закодированный путь"
        self.path = _url_parse(self.raw_path)
        "Докодированный путь"
        self.http_ver = first[2]
        "Версия HTTP"
        self._raw_headers = headers.split(b"\r\n", 1)[1]
        self.headers = _get_headers(self._raw_headers)
        "Заголовки запроса"
        self.auth = True, True
        "Статус авторизациии"
        self.files = []
        "Файлы запроса"
        self.raw_data = None
        "Сырые данные"
        self.cookies = _get_cookies(self.headers.get("cookie", ""))
        "Куки запроса"
        if self.method.lower() != "get":
            self.raw_data = data
            self.files = File.get(self._raw_headers, self.raw_data)
            try:
                self._data_to_dict(data)
            except Exception:  # TODO четкий список исключений
                logging.critical(traceback.format_exc())

    def _data_to_dict(self, data: bytes):
        try:
            self.data = json.loads(data)
        except json.decoder.JSONDecodeError:
            self.data = {}


class Response():  # pylint: disable=too-many-instance-attributes,too-few-public-methods
    """Класс по умолчанию, хранящий в себе методы и свойства для работы с ответом пользователю."""

    def __init__(self,
                 code: int = 200,
                 data: dict | bytes | str | File | None = None,
                 headers: Optional[dict] = None,
                 # Имеет максимальный приоритет
                 content_type: Optional[str] | None = None,
                 cookies: Optional[dict] = None
                 ):  # pylint: disable=too-many-arguments
        """Ответ сервера.

        Args:
            code (int, optional): код ответа. Defaults to 200
            data (Any, optional): данные. Defaults to None
            headers (Optional[dict], optional): Заголовки.Defaults to {}
            content_type (Optional[str], optional): тип контента. Defaults to "text/plain"
            cookies (Optional[dict], optional): куки запроса. Defaults to {}
        """
        self.code = code
        "HTTP код ответа"
        self.data = data or "empty"
        "Данные"
        self.headers: dict[str, str] = headers or {}
        "Заголовки ответа"
        self.cookies = cookies or {}
        "Куки ответа"
        self._data_type: str
        self.content_type: str | None = content_type
        "Тип отправляемых данных"
        self._content_type: str
        self._raw_data: bytes
        self._raw_response: bytes

    def _generate_raw(self):
        self._data_type = type(self.data).__qualname__
        match self._data_type:
            case 'dict':
                self._raw_data = json.dumps(
                    self.data,
                    indent=2,
                    default=str,
                ).encode()
                self._content_type = TYPES['json']

            case 'bytes':
                self._raw_data = self.data
                self._content_type = TYPES['bin']
            case 'str':
                self._raw_data = self.data.encode()
                self._content_type = TYPES['html']

            case 'File':
                self._raw_data = self.data.data
                self._content_type = TYPES.get(
                    self.data.filename.split(".")[-1], TYPES["txt"])
            case _:
                logging.warning(
                    "Unknown return type %s.", self._data_type)
                self._raw_data = str(self.data).encode()
                self._content_type = TYPES['txt']

        if self.content_type:
            self.content_type = TYPES.get(self.content_type, self.content_type)
        else:
            self.content_type = self._content_type

        raw_first = f'HTTP/1.1 {self.code} {CODES.get(self.code, "Done")}'.encode(
        )

        raw_headers = _set_headers(
            DEFAULT_HEADERS
        ).replace(b"{Server}", SERVER.encode()
                  ).replace(b"{DateTime}", datetime.datetime.now(
                  ).strftime('%a, %d %b %Y %H:%M:%S GMT').encode()
        ).replace(b"{ContentLength}", str(len(self._raw_data)).encode()
                  ).replace(b"{ContentType}", self.content_type.encode())

        raw_headers += _set_headers(self.headers)
        raw_headers += _set_headers(CORS_HEADERS)
        for key in self.cookies.keys():
            raw_headers += _set_headers(
                {'Set-Cookie': key + '=' + self.cookies[key]})

        self._raw_response = raw_first+b'\r\n'+raw_headers + \
            b"\r\n"+self._raw_data+b"\r\n\r\n"

    def send(self, conn: socket.socket):
        """Метод, отправляющий ответ по спецификации http.

        Args:
            conn (socket.socket): сокет для отправки данных
        """
        self._generate_raw()
        conn.send(self._raw_response)
        conn.close()
        logging.info("Returned - %s, %s.", self.code, self.content_type)
