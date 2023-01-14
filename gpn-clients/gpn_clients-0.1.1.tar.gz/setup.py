# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gpn_clients',
 'gpn_clients.clients.nsi.v1',
 'gpn_clients.core',
 'gpn_clients.models',
 'gpn_clients.utils']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.2,<2.0.0', 'setuptools>=65.7.0,<66.0.0']

setup_kwargs = {
    'name': 'gpn-clients',
    'version': '0.1.1',
    'description': 'Клиенты для получения данных из источников внутри ГПН',
    'long_description': '# 🀣 🅖🅟🅝 🅲🅻🅸🅴🅽🆃🆂 🀣\n\n![Code Coverage](https://img.shields.io/badge/Coverage-90%25-green.svg)\n\nГПН Клиенты предоставляющие интерфейс для работы с источниками данных.\n\n## Базовое использование\n\nКонфигурация клиента на примере клиента NSI\n',
    'author': 'Chumakov Mikhail Dmitrievich',
    'author_email': 'i@m-chumakov-dev.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
