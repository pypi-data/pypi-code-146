# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sciluigi']

package_data = \
{'': ['*']}

install_requires = \
['luigi>=3.1.1,<4.0.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'sciluigi',
    'version': '0.10.0',
    'description': '',
    'long_description': 'None',
    'author': 'y',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
