# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['BETDisk']

package_data = \
{'': ['*']}

install_requires = \
['scipy>=1.9.3,<2.0.0']

setup_kwargs = {
    'name': 'flow360-betdisk',
    'version': '0.1.12',
    'description': '',
    'long_description': 'None',
    'author': 'Flexcompute',
    'author_email': 'support@flexcompute.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
