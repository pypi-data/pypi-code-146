# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['m3query']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'm3query',
    'version': '0.1.2',
    'description': 'A wrapper around the JayDeBeApi library to connect to M3. Should not be distributed due to the ownership of the driver.',
    'long_description': None,
    'author': 'Kim Timothy Engh',
    'author_email': 'kim.timothy.engh@epiroc.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
