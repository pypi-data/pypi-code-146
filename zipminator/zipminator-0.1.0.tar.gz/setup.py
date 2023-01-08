# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zipminator']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.24.1,<2.0.0', 'pandas>=1.5.2,<2.0.0']

setup_kwargs = {
    'name': 'zipminator',
    'version': '0.1.0',
    'description': 'zipminator is a lightweight python package with two main functionalities; Zipndel or Unzipndel, for zipping or unzipping a password-protected pandas DataFrame file, and then deleting the original file.',
    'long_description': None,
    'author': 'QDaria',
    'author_email': 'mo@qdaria.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
