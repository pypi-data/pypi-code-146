# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['toto_client']

package_data = \
{'': ['*']}

install_requires = \
['google-auth>=2.15.0,<3.0.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'toto-client',
    'version': '0.0.8',
    'description': '',
    'long_description': 'None',
    'author': 'R2 Factory',
    'author_email': 'contact@r2-factory.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.8.13',
}


setup(**setup_kwargs)
