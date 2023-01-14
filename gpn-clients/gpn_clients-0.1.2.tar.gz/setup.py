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
    'version': '0.1.2',
    'description': 'Клиенты для получения данных из источников внутри ГПН',
    'long_description': '# 🀣 🅖🅟🅝 🅲🅻🅸🅴🅽🆃🆂 🀣\n\n![Code Coverage](https://img.shields.io/badge/Coverage-90%25-green.svg)\n\nГПН Клиенты предоставляющие интерфейс для работы с источниками данных.\n\n## Базовое использование\n\n**Конфигурация** клиента на примере клиента NSI:\n\n```python\nfrom gpn_clients.core.config import nsi_config\n\n\nNSI_HOST: str = "https://test-nsi-host-228.com"\nNSI_PORT: int = 443\n\n# Конфигурация клиента\nnsi_config.set_config(\n    host=NSI_HOST,\n    port=NSI_PORT,\n)\n```\n\nПосле конфигурации клиента можно использовать его методы.\nИспользование интерфейсов NSI **Алгоритмов**:\n\n```python\nfrom pydantic import HttpUrl\n\nfrom gpn_clients.clients.nsi.v1.algorithms import (\n    AbstractAlgorithms,\n    NSIAlgorithms,\n)\n\n\nnsi_algorithms: AbstractAlgorithms = NSIAlgorithms()\n\n# Получение URL для списка алгоритмов\nalgorithms: HttpUrl = nsi_algorithms.get_all()\n\n# Получение URL для алгоритма по его ID\nalgorithm: HttpUrl = nsi_algorithms.get_by_id(algorithm_id=1)\n```\n',
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
