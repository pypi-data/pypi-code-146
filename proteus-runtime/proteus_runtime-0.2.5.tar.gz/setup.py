# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['proteus', 'proteus.calculator']

package_data = \
{'': ['*']}

install_requires = \
['azure-storage-blob>=12.14.1,<13.0.0',
 'certifi>=2022.12.07,<2023.0.0',
 'multipart>=0.2.4,<0.3.0',
 'numpy>=1.23.3,<2.0.0',
 'parglare>=0.16.0,<0.17.0',
 'python-json-logger>=2.0.4,<3.0.0',
 'requests>=2.28.1,<3.0.0',
 'setuptools>=65.0.0,<66.0.0']

setup_kwargs = {
    'name': 'proteus-runtime',
    'version': '0.2.5',
    'description': '',
    'long_description': 'None',
    'author': 'None',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
