# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mock-aiohttp']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.3,<4.0.0',
 'pytest-asyncio>=0.20.3,<0.21.0',
 'pytest>=7.2.0,<8.0.0']

setup_kwargs = {
    'name': 'mock-aiohttp',
    'version': '0.1.1',
    'description': 'Create a mock for aiohttp.ClientSession',
    'long_description': '# mock-aiohttp\n\nAttempting to create a reusable mock for testing with `aiohttp.ClientSession()`.\n\nCurrently in: Pre-alpha (use at your own risk)\n\nUse `poetry install` locally to setup for development\n',
    'author': 'fitzypop',
    'author_email': '32967490+fitzypop@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/fitzypop/mock-aiohttp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
