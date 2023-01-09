# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quera', 'quera.utils']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0', 'xattr>=0.9.9,<0.10.0']

setup_kwargs = {
    'name': 'quera',
    'version': '0.1.16',
    'description': '',
    'long_description': 'None',
    'author': 'Quera Team',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
