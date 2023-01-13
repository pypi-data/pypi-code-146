# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wydyf']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'matplotlib>=3.6.3,<4.0.0',
 'openpyxl>=3.0.10,<4.0.0',
 'pandas>=1.5.2,<2.0.0',
 'rich>=13.0.1,<14.0.0']

setup_kwargs = {
    'name': 'wydyf',
    'version': '0.0.1',
    'description': '未央书院答疑坊',
    'long_description': '## 未央书院答疑坊\n',
    'author': 'Qin Li',
    'author_email': 'liblaf@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://liblaf.github.io/wydyf/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
