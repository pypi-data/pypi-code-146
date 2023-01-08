import os
from typing import Callable

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


def _dedupe(items: list[str]):
    seen = set()
    for item in items:
        short = item[0:2]
        if short not in seen:
            yield short
            seen.add(item)


def translator(accept_language: str = Header(default=None)) -> Callable[[str], str]:
    locales: dict[str, float] = {}
    if accept_language is None:
        locales[_settings.i18n_default_locale] = 1
    elif ',' not in accept_language:
        if ';' not in accept_language:
            locales[accept_language] = 1
        else:
            locale, q = accept_language.split(';')
            _, q = q.split('=')
            locales[locale] = int(q)
    else:
        _locales = accept_language.split(',')
        for locale in _locales:
            if ';' not in locale:
                locales[locale] = 1
                continue
            locale, q = locale.split(';')
            _, q = q.split('=')
            locales[locale] = int(q)
    sorted_locales = [x[0] for x in sorted(locales.items(), key=lambda x: x[1], reverse=True)]
    sorted_locales += list(_dedupe(sorted_locales))

    def t(code: str) -> str:
        package = _settings.i18n_default_package
        if ':' in code:
            package, code = code.split(':')

        package: dict = _messages.get(package)
        if package is None:
            return code

        messages: dict | str | None = None
        for t_locale in sorted_locales:
            messages = package.get(t_locale)
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

    return t
