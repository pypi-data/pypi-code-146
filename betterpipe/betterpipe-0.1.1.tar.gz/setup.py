# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['betterpipe']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'betterpipe',
    'version': '0.1.1',
    'description': 'Betterpipe: Break free from limited observability in DevOps/MLOps platforms. Pipe .py file data to external data warehouse for complete control over model performance. Easily troubleshoot and make informed decisions. ',
    'long_description': None,
    'author': 'Clerkie AI',
    'author_email': 'clerkieai@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
