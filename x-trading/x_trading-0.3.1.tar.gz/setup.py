# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['x_trading', 'x_trading._pp']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0']

entry_points = \
{'console_scripts': ['x = x_trading.x:x']}

setup_kwargs = {
    'name': 'x-trading',
    'version': '0.3.1',
    'description': 'Comandos úteis para o trading',
    'long_description': '',
    'author': 'Valmir Franca',
    'author_email': 'vfranca3@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/vfranca/x-trading',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
