# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ghclone']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['ghclone = ghclone:ghclone.main']}

setup_kwargs = {
    'name': 'ghclone',
    'version': '1.0.0',
    'description': 'A command line utility to interactively search and clone GitHub repositories',
    'long_description': None,
    'author': 'Tibo Clausen',
    'author_email': 'tibo.clausen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
