"""Класс для методов управления сервером."""
import re
import os
import sys
import time
import socket
import logging
import traceback
from typing import Callable, Any
from threading import Thread

from .classes import Request, Response
from .utils import _get_data
from .exceptions import InvalidParametersCount, AlreadyUsedException


def _err404(req: Request):
    return Response(404, f"Error: path {req.path} not found.")


def _err500(req: Request, exception: Exception):
    return Response(500, f"Error: while working with {req.path} handled exception: {exception}.")


def _auth_funk(req: Request):
    return True, req.path


class Server():
    """Класс для управления конфигурацией и методами сервера."""
    @staticmethod
    def _res_to_response(res: Any, code=200) -> Response:
        match type(res).__qualname__:
            case "Response":
                if isinstance(res, Response):
                    return res
                ctype = res.headers.pop('Content-Type', "text/html")
                res.headers.pop('Server', '')
                res.headers.pop('Date', '')
                res.headers.pop('Transfer-Encoding', "")
                res.headers.pop("Access-Control-Allow-Origin", "")

                return Response(
                    res.status_code, res.content,
                    dict(res.headers), ctype, dict(res.cookies)
                )
            case "int":
                return Response(res)
            case "tuple":
                if isinstance(res[0], int):
                    return Response(*res)
                return Response(code, *res)
            case _:
                return Response(code, res)

    def _bind(self, regex, func, auth_funk):
        regex = re.compile(regex)
        if func.__qualname__ not in self._funcs:
            need = regex.groups + 1
            if need != func.__code__.co_argcount:
                raise InvalidParametersCount(
                    func, need, func.__code__.co_argcount)
            self._bindes[re.compile(regex)] = func, auth_funk
            self._funcs[func.__qualname__] = func
        else:
            raise AlreadyUsedException(func)

    def bind(self, path_regex: str, auth_funk: Callable = _auth_funk):
        """Метод для назначения обработчика для конкретного адреса с учетом регулярных выражений.

        Args:
            path_regex (str): регулярное выражение - путь
            auth_funk (Callable, optional): функция для проверки авторизации
        """
        def _wrapper(func):
            self._bind(path_regex, func, auth_funk)
        return _wrapper

    def ebind(self, path_regex, auth_funk=_auth_funk):
        """Метод для назначения обработчика для конкретного адреса \
            с учетом псевдо-регулярных выражений вида <param>.

        Args:
            path_regex (str, optional): псевдо-регулярное выражение - путь
            auth_funk (_type_, optional): функция для проверки авторизации
        """
        patterns = re.findall(r'(<\w+>)+', path_regex)
        for _ in patterns:
            if len(_) > 0:
                path_regex = path_regex.replace(_, r'(\w+)')

        def _wrapper(func):
            self._bind(path_regex, func, auth_funk)
        return _wrapper

    def _handler(self, conn):
        data = _get_data(conn)
        req = Request(data[0], data[1])
        logging.info(time.strftime("%H:%M:%S", time.gmtime())+" " + req.path)
        response = None
        try:
            for bind, (bhandler, auth_funk) in self._bindes.items():
                match = bind.fullmatch(req.path)
                if match:
                    req.auth = auth_funk(req)
                    if isinstance(req.auth, Response):
                        response = req.auth
                    else:
                        response = Server._res_to_response(
                            bhandler(req, *match.groups()))
                    break
            else:
                response = _err404(req)
        except Exception as exception:  # pylint: disable=broad-except
            logging.critical(traceback.format_exc())
            response = _err500(req, exception)

        response.headers = response.headers | self.default_headers
        response.send(conn)

    def __init__(self,
                 host="0.0.0.0",
                 port=3000,
                 force_bind=False,
                 default_headers: dict[str, str] | None = None
                 ):
        """Сервер, принимающий запросы

        Args:
            host (str, optional): адресс сервера. Defaults to "0.0.0.0"
            port (int, optional): порт сервера. Defaults to 3000
            force_bind (bool, optional): принудительно освобождать порт. Defaults to False
            default_headers (dict, optional): заголовки ответов по умолчанию. Defaults to {}
        """
        self.host = host
        self.port = port
        self.force_bind = force_bind
        self.default_headers = default_headers or {}
        self._bindes: dict[str, tuple[Callable, Callable]] = {}
        self._funcs: dict[str, Callable] = {}
        self._sock: socket.socket

    def start(self):
        """Метод запускающий прослушивание сервера."""
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self._sock.bind((self.host, self.port))
            self._sock.listen(10)
            try:
                logging.info("Server started on http://%s:%s/",
                             self.host, self.port)
                while True:
                    conn, _ = self._sock.accept()
                    Thread(
                        target=self._handler,
                        args=(
                            conn,
                        ),
                    ).start()
            except KeyboardInterrupt:
                self._sock.shutdown(1)
                logging.info("Exited")
        except OSError as exception:
            if self.force_bind and ("98" in str(exception)):
                os.system(f"fuser -k {self.port}/tcp")
                time.sleep(0.01)
                self.start()
            else:
                logging.critical(traceback.format_exc())

        sys.exit(1)
