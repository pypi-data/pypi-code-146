# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_admin_cli']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'flask-admin-cli',
    'version': '0.1.0',
    'description': '',
    'long_description': '# flask admin cli',
    'author': 'Mario Hernandez',
    'author_email': 'mariofix@proton.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
