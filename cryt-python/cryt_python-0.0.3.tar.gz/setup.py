# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cryt']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.3,<4.0.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'cryt-python',
    'version': '0.0.3',
    'description': '',
    'long_description': '',
    'author': 'Aleksander Skiridomov',
    'author_email': 'aleksander.skiridomov@cryt.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
