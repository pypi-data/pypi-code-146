# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iotree', 'iotree.cli', 'iotree.core', 'iotree.utils']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=7.2.0,<8.0.0',
 'pyyaml>=6.0,<7.0',
 'rich>=10.11.0,<13.0.0',
 'toml>=0.10.2,<0.11.0',
 'typer[all]>=0.7.0,<0.8.0',
 'xmltodict>=0.13.0,<0.14.0']

entry_points = \
{'console_scripts': ['iotree = iotree.cli:app']}

setup_kwargs = {
    'name': 'iotree',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Arno V',
    'author_email': 'bcda0276@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
