import os

import yaml
from fastapi import Header

from .config import get_settings

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

_settings = get_settings()
_allowed_ext = ('yaml', 'yml')

_messages = {}


def init():
    loading_dir = os.path.join(os.getcwd(), _settings.i18n_loading_dir)
    for root, dirs, files in os.walk(loading_dir):
        for file in files:
            file_name, ext = file.split('.')

            if ext not in _allowed_ext:
                continue

            name_list = file_name.split('_')
            if len(name_list) == 2:
                package, locale = name_list
            else:
                package = name_list[0]
                locale = _settings.i18n_default_locale

            with open(os.path.join(root, file), 'r') as stream:
                loaded: dict = yaml.load(stream, Loader)
                if _messages.get(package) is None:
                    _messages[package] = {}
                _messages[package][locale] = loaded


class Translator:
    locales: dict[str, float]
    _sorted_locales: list[str] = None

    def __init__(self, accept_language: str = Header(default=None)):
        if accept_language is None:
            self.locales[_settings.i18n_default_locale] = 1
            return

        if ',' not in accept_language:
            if ';' not in accept_language:
                self.locales[accept_language] = 1
            else:
                locale, q = accept_language.split(';')
                _, q = q.split('=')
                self.locales[locale] = int(q)
            return

        locales = accept_language.split(',')
        for locale in locales:
            if ';' not in locale:
                self.locales[locale] = 1
                continue
            locale, q = locale.split(';')
            _, q = q.split('=')
            self.locales[locale] = int(q)
        self.locales = {x[0]: x[1] for x in sorted(self.locales.items(), key=lambda x: x[1], reverse=True)}

    def t(self, code: str) -> str:
        package = _settings.i18n_default_package
        if ':' in code:
            package, code = code.split(':')
        package: dict = _messages.get(package)
        if package is None:
            return code
        messages: dict | str | None = None
        for locale in self.get_sorted():
            messages = package.get(locale)
            if messages is not None:
                break
        if messages is None:
            return code

        keys = code.split('.')
        for key in keys:
            messages = messages.get(key)
            if messages is None:
                return code
            if isinstance(messages, dict):
                continue
            return messages

    def get_sorted(self):
        if self._sorted_locales is None:
            self._sorted_locales = [x[0] for x in sorted(self.locales.items(), key=lambda x: x[1], reverse=True)]

        return self._sorted_locales
