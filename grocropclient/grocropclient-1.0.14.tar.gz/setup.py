# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['grocropclient']

package_data = \
{'': ['*']}

install_requires = \
['fuzzywuzzy', 'groclient', 'numpy', 'pandas']

setup_kwargs = {
    'name': 'grocropclient',
    'version': '1.0.14',
    'description': "Python client library for accessing Gro Intelligence's US crop insights",
    'long_description': 'The Gro US Crop API Client is a Python library to help with the discovery and retrieval of data series related to US crops.\n\nThe library is written on top of the [Gro Python Client API](https://github.com/gro-intelligence/api-client)\nand offers a set of convenience methods and constants to make the use of the Gro API faster and simpler.\n\nThe use of the Gro US Crop API Client requires a Gro account with API access.\nVisit our [website](https://gro-intelligence.com/platform/api) for more information.\n',
    'author': 'Gro Intelligence developers',
    'author_email': 'dev@gro-intelligence.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.gro-intelligence.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
