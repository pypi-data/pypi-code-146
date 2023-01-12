# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['magnet_data',
 'magnet_data.currencies',
 'magnet_data.holidays',
 'magnet_data.migrations']

package_data = \
{'': ['*']}

install_requires = \
['django>=2.2']

setup_kwargs = {
    'name': 'django-magnet-data',
    'version': '1.1.2',
    'description': 'An API client for data.magnet.cl',
    'long_description': None,
    'author': 'Ignacio Munizaga',
    'author_email': 'muni@magnet.cl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/magnet-cl/django-magnet-data',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
