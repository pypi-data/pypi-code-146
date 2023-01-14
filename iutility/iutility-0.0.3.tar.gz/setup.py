# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iutility',
 'iutility.clean',
 'iutility.git',
 'iutility.key',
 'iutility.update']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'ishutils>=0.0.3,<0.0.4',
 'toml-sort>=0.20.1,<0.21.0',
 'tomlkit>=0.11.6,<0.12.0']

setup_kwargs = {
    'name': 'iutility',
    'version': '0.0.3',
    'description': 'My Utils',
    'long_description': '# iutility\n\nMy Utils\n',
    'author': 'Qin Li',
    'author_email': 'liblaf@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://liblaf.github.io/iutility/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
