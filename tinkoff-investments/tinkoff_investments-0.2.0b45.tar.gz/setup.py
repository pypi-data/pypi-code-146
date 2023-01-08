# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tinkoff',
 'tinkoff.invest',
 'tinkoff.invest.caching',
 'tinkoff.invest.caching.instruments_cache',
 'tinkoff.invest.caching.market_data_cache',
 'tinkoff.invest.grpc',
 'tinkoff.invest.market_data_stream',
 'tinkoff.invest.retrying',
 'tinkoff.invest.retrying.aio',
 'tinkoff.invest.retrying.sync',
 'tinkoff.invest.sandbox',
 'tinkoff.invest.strategies',
 'tinkoff.invest.strategies.base',
 'tinkoff.invest.strategies.moving_average',
 'tinkoff.invest.strategies.plotting']

package_data = \
{'': ['*']}

install_requires = \
['cachetools>=5.2.0,<6.0.0',
 'grpcio>=1.39.0,<2.0.0',
 'protobuf>=3.20.2,<4.0.0',
 'pydantic>=1.9.2,<2.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'tinkoff>=0.1.1,<0.2.0']

extras_require = \
{'all': ['matplotlib>=3.5.1,<4.0.0',
         'mplfinance>=0.12.8-beta.9,<0.13.0',
         'numpy>=1.22.2,<2.0.0',
         'pandas>=1.4.0,<2.0.0']}

setup_kwargs = {
    'name': 'tinkoff-investments',
    'version': '0.2.0b45',
    'description': '',
    'long_description': '# Tinkoff Invest\n\n[![PyPI](https://img.shields.io/pypi/v/tinkoff-investments)](https://pypi.org/project/tinkoff-investments/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tinkoff-investments)](https://www.python.org/downloads/)\n\nДанный репозиторий предоставляет клиент для взаимодействия с торговой платформой [Тинькофф Инвестиции](https://www.tinkoff.ru/invest/) на языке Python.\n\n- [Документация](https://tinkoff.github.io/invest-python/)\n- [Основной репозиторий с документацией](https://github.com/Tinkoff/investAPI)\n- [Документация для разработчиков](https://tinkoff.github.io/investAPI/)\n\n## Начало работы\n\n<!-- termynal -->\n\n```\n$ pip install tinkoff-investments\n```\n\n## Возможности\n\n- &#9745; Синхронный и асинхронный GRPC клиент\n- &#9745; Возможность отменить все заявки\n- &#9745; Выгрузка истории котировок "от" и "до"\n- &#9745; Кеширование данных\n- &#9745; Торговая стратегия\n\n## Как пользоваться\n\n### Получить список аккаунтов\n\n```python\nfrom tinkoff.invest import Client\n\nTOKEN = \'token\'\n\nwith Client(TOKEN) as client:\n    print(client.users.get_accounts())\n```\n\n### Переопределить target\n\nВ Tinkoff Invest API есть два контура - "боевой", предназначенный для исполнения ордеров на бирже и "песочница", предназначенный для тестирования API и торговых гипотез, заявки с которого не выводятся на биржу, а исполняются в эмуляторе.\n\nПереключение между контурами реализовано через target, INVEST_GRPC_API - "боевой", INVEST_GRPC_API_SANDBOX - "песочница"\n\n```python\nfrom tinkoff.invest import Client\nfrom tinkoff.invest.constants import INVEST_GRPC_API\n\nTOKEN = \'token\'\n\nwith Client(TOKEN, target=INVEST_GRPC_API) as client:\n    print(client.users.get_accounts())\n```\n\n> :warning: **Не публикуйте токены в общедоступные репозитории**\n<br/>\n\nОстальные примеры доступны в [examples](https://github.com/Tinkoff/invest-python/tree/main/examples).\n\n## Contribution\n\nДля тех, кто хочет внести свои изменения в проект.\n\n- [CONTRIBUTING](https://github.com/Tinkoff/invest-python/blob/main/CONTRIBUTING.md)\n\n## License\n\nЛицензия [The Apache License](https://github.com/Tinkoff/invest-python/blob/main/LICENSE).\n',
    'author': 'Danil Akhtarov',
    'author_email': 'd.akhtarov@tinkoff.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Tinkoff/invest-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
