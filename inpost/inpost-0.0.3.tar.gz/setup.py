# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['inpost', 'inpost.static', 'static']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.4.0,<10.0.0',
 'aiohttp>=3.8.1,<4.0.0',
 'arrow>=1.2.3,<2.0.0',
 'qrcode>=7.3.1,<8.0.0']

setup_kwargs = {
    'name': 'inpost',
    'version': '0.0.3',
    'description': 'Asynchronous InPost package allowing you to manage existing incoming parcels without mobile app',
    'long_description': 'Fully async Inpost API library\n',
    'author': 'loboda4450',
    'author_email': 'loboda4450@gmail.com',
    'maintainer': 'loboda4450',
    'maintainer_email': 'loboda4450@gmail.com',
    'url': 'https://github.com/IFOSSA/inpost-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
