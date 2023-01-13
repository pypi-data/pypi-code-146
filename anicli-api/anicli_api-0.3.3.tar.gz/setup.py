# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['anicli_api',
 'anicli_api.decoders',
 'anicli_api.extractors',
 'anicli_api.tools']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2', 'httpx>=0.23.0,<0.24.0', 'yt-dlp>=2023.1.6,<2024.0.0']

setup_kwargs = {
    'name': 'anicli-api',
    'version': '0.3.3',
    'description': 'Anime extractor api implementation',
    'long_description': '# anicli-api\n[![CI](https://github.com/vypivshiy/anicli-api/actions/workflows/ci.yml/badge.svg)](https://github.com/vypivshiy/anicli-api/actions/workflows/ci.yml)\n[![Documentation Status](https://readthedocs.org/projects/anicli-api/badge/?version=latest)](https://anicli-api.readthedocs.io/en/latest/?badge=latest)\n\nПрограммный интерфейс парсера аниме с различных источников.\n\nПрисутствует поддержка sync и async методов с помощью `httpx` библиотеки, для получения информации и прямых ссылок \nна видео.\n\n# install\n`pip install anicli-api`\n\n# Overview\nМодуль экстрактора имеют следующую структуру пошагового получения объекта:\n```shell\n# Extractor works schema:\n    [Extractor]\n        | search(<query>)/ongoing()  -> List[SearchResult | Ongoing]\n        V                           \n  [SearchResult | Ongoing]          \n         | get_anime()  -> AnimeInfo\n         V                          \n    [AnimeInfo]                     \n        | get_episodes()  -> List[Episode]  \n        V                           \n    [Episode]                      \n        | get_videos()  -> List[Video]              \n        V                           \n    [Video]\n        | get_source()  -> MetaVideo or Str\n        V\n    MetaVideo(type, quality, url, extra_headers) or url\n```\n\n# Quickstart example\nСмотрите примеры [examples](examples) и [документации](https://anicli-api.readthedocs.io/en/latest/index.html)!\n\n# Примечания\n\nПроект разработан преимущественно на личное, некоммерческое использование на стороне клиента. \nАвтор проекта не несет ответственности за поломки, убытки в высоко нагруженных проектах и решение\nпредоставляется "Как есть" в соответствии с [MIT](LIENSE) лицензией.\n\nЕсли вы всё же решили этот проект использовать в **production** условиях, \nто выстаивайте архитектуру своих проектов **на предварительный сбор информации** \n(например, полученные данные сохранять в базу данных и оттуда позже получать), \nтак как большинство парсеров работает в обход официальных методов и применяются такие библиотеки как re, bs4. \n\nСледовательно, могут быть проблемы от производительности, до получения ошибок по типу 403 (срабатывание ddos защиты) или \n502 (доступа к сайту запрещён).\n\n**Этот проект не включает инструменты кеширования и сохранения всех полученных данных, только эндпоинты \nс готовой реализацией архитектуры парсеров**\n\n# DEV\n [DEV](DEV.MD)\n\n# Contributing\n[CONTRIBUTING](CONTRIBUTING.MD)\n\n# TODO\n* ~~CI CD автотестов~~\n~~* Поправить sphinx документацию~~\n* Получение видео по ссылке (like yt-dlp)\n* расширенный поиск (по жанрам, годам, etc)\n* улучшение документации\n* Продумать стандартизацию атрибутов в экстракторах (если такое реально?)\n* ~~asyncio tests~~\n* ~~coverage~~\n* ~~добавить примеры~~\n* ~~Написать документацию для high level применения пока на уровне example примеров~~\n* ~~Написать документацию для low level разработки экстракторов~~\n* ~~Дописать asyncio методы для animego~~\n* ~~Портировать anilibria, animevost, animania экстракторы из старого проекта~~\n',
    'author': 'Georgiy aka Vypivshiy',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
