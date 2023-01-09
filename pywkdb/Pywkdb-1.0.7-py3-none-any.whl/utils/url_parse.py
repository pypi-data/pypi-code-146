#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kombu.utils.url import url_to_parts


class UrlParse(object):

    def __init__(self, url):
        self._scheme, self._host, self._port, self._user, self._password, self._path, self._query = url_to_parts(url)

    @property
    def scheme(self) -> str:
        return self._scheme

    @property
    def hostname(self) -> str:
        return self._host

    @property
    def port(self) -> int:
        return self._port

    @property
    def username(self) -> str:
        return self._user

    @property
    def password(self) -> str:
        return self._password

    @property
    def path(self) -> str:
        return self._path

    @property
    def query(self) -> dict:
        return self._query

    def __str__(self):
        import json
        return json.dumps({
            "scheme": self.scheme,
            "hostname": self.hostname,
            "port": self.port,
            "username": self.username,
            "password": self.password,
            "path": self.path,
            "query": self.query
        }, indent=2)


if __name__ == '__main__':
    pass
