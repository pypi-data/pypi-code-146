# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pisql', 'pisql.cli', 'pisql.core', 'pisql.utils']

package_data = \
{'': ['*'], 'pisql': ['assets/*', 'assets/data/*', 'assets/sql/*']}

install_requires = \
['iotree>=0.1.14,<0.2.0', 'polars>=0.15.13,<0.16.0', 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['pisql = pisql.main:app']}

setup_kwargs = {
    'name': 'pisql',
    'version': '0.1.14',
    'description': '',
    'long_description': '',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
