# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kodexa_cli']

package_data = \
{'': ['*'], 'kodexa_cli': ['templates/*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'click==8.1.3',
 'flake8>=6.0.0,<7.0.0',
 'kodexa>=6.0.116,<7.0.0',
 'mypy>=0.991,<0.992',
 'rich==12.5.1']

setup_kwargs = {
    'name': 'kodexa-cli',
    'version': '6.0.0',
    'description': '',
    'long_description': '# kodexa-cli',
    'author': 'Romar Cablao',
    'author_email': 'rcablao@kodexa.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
