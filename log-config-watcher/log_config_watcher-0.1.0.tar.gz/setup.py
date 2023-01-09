# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['log_config_watcher']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'log-config-watcher',
    'version': '0.1.0',
    'description': 'Watches your logging configuration file for change and applies them without requiring an application restart',
    'long_description': None,
    'author': 'Robert DeRose',
    'author_email': 'rderose@checkpt.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
