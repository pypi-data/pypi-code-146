# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kawapack']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.4.0,<10.0.0',
 'UnityPy>=1.9.24,<2.0.0',
 'pycryptodome>=3.16.0,<4.0.0',
 'pymongo>=4.3.3,<5.0.0']

setup_kwargs = {
    'name': 'kawapack',
    'version': '0.7.0',
    'description': 'Utility for extracting Arknights assets',
    'long_description': 'None',
    'author': 'astral4',
    'author_email': '88992929+astral4@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
