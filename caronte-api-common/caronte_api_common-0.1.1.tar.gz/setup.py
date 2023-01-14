# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['caronte', 'caronte.common', 'caronte.common.interfaces']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'caronte-api-common',
    'version': '0.1.1',
    'description': 'Common components and modules to integrate Caronte layers',
    'long_description': '# Caronte-application',
    'author': 'Giovani Liskoski Zanini',
    'author_email': 'giovanilzanini@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
