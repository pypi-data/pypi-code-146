# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bk7231tools',
 'bk7231tools.analysis',
 'bk7231tools.crypto',
 'bk7231tools.serial']

package_data = \
{'': ['*']}

install_requires = \
['pycryptodomex>=3.16.0,<4.0.0', 'pyserial>=3.5,<4.0']

entry_points = \
{'console_scripts': ['bk7231tools = bk7231tools:cli',
                     'bktools = bk7231tools:cli']}

setup_kwargs = {
    'name': 'bk7231tools',
    'version': '1.2.5',
    'description': 'Tools to interact with and analyze artifacts for BK7231 MCUs',
    'long_description': 'None',
    'author': 'Khaled Nassar',
    'author_email': 'kmhnassar@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
