# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kubectlgetall']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0']

entry_points = \
{'console_scripts': ['kubectlgetall = kubectlgetall.cli:cli']}

setup_kwargs = {
    'name': 'kubectlgetall',
    'version': '0.1.1',
    'description': 'Get a list of CRs for cluster CRDs in a namespace',
    'long_description': None,
    'author': 'Jim Fitzpatrick',
    'author_email': 'jimfity@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Boomatang/kubectlgetall',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
