# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['statespace', 'statespace.models', 'statespace.processors']

package_data = \
{'': ['*']}

install_requires = \
['filterpy>=1.4,<2.0',
 'matplotlib>=3.6,<4.0',
 'numpy>=1.24,<2.0',
 'scipy>=1.10,<2.0']

setup_kwargs = {
    'name': 'statespace',
    'version': '1.6.5',
    'description': '',
    'long_description': 'None',
    'author': 'noah smith',
    'author_email': 'noah@statespace.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
