# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nuke']

package_data = \
{'': ['*']}

install_requires = \
['click>=6.7', 'crayons>=0.1.2', 'rich>=12.6.0,<13.0.0']

setup_kwargs = {
    'name': 'nuke',
    'version': '2.5.2',
    'description': 'Command line tool for nuking a directory 💥',
    'long_description': 'None',
    'author': 'Varun Agrawal',
    'author_email': 'varagrawal@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0.0',
}


setup(**setup_kwargs)
