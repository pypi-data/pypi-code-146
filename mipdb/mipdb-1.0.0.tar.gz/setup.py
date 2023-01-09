# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mipdb']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.3.0,<1.4.0',
 'click>=8,<9',
 'pandas>=1.5.2,<1.6.0',
 'pandera>=0.13.4,<0.14.0',
 'pymonetdb<1.5',
 'sqlalchemy_monetdb>=1.0.0,<1.1.0']

entry_points = \
{'console_scripts': ['mipdb = mipdb.commands:entry']}

setup_kwargs = {
    'name': 'mipdb',
    'version': '1.0.0',
    'description': '',
    'long_description': 'None',
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
