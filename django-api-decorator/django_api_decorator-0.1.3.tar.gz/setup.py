# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_api_decorator',
 'django_api_decorator.management',
 'django_api_decorator.management.commands']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3', 'pydantic>=1.10.2,<2.0.0']

setup_kwargs = {
    'name': 'django-api-decorator',
    'version': '0.1.3',
    'description': 'A collection of tools to build function based Django APIs',
    'long_description': '<h1 align="center">\n  Django API Decorator\n</h1>\n\n<p align="center">\n  A collection of tools to build function based Django APIs.\n</p>\n\n> **Warning**\n> This project is still in early development. Expect breaking changes.\n\n## Installation\n\nDjango API Decorator can be installed from\n[PyPI](https://pypi.org/project/django-api-decorator):\n\n`pip install django-api-decorator`\n',
    'author': 'Oda',
    'author_email': 'tech@oda.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kolonialno/django-api-decorator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
