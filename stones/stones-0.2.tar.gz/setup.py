# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stones']

package_data = \
{'': ['*']}

install_requires = \
['lmdb==1.3.0']

setup_kwargs = {
    'name': 'stones',
    'version': '0.2',
    'description': 'Library for Persistent key-value containers, compatible with Python dict',
    'long_description': 'None',
    'author': 'Cristi Constantin',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/croqaz/Stones',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
