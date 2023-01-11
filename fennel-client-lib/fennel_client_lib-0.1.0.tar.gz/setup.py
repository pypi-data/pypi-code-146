# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fennel_client_lib']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'fennel-client-lib',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Aditya Nambiar',
    'author_email': 'adityanambiar@fennel.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
