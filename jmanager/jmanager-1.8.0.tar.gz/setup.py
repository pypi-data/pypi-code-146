# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jmanager']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'jupyterlab>=3.5.2,<4.0.0']

entry_points = \
{'console_scripts': ['jmanager = jmanager.cli:main']}

setup_kwargs = {
    'name': 'jmanager',
    'version': '1.8.0',
    'description': 'A lightweight Jupyter process manager',
    'long_description': None,
    'author': 'Yasunori Horikoshi',
    'author_email': 'hotoku@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
