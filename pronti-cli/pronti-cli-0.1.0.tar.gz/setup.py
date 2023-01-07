# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pronti_cli']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pronti-cli',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Oscar Bahamonde',
    'author_email': '107950590+obahamonde@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
