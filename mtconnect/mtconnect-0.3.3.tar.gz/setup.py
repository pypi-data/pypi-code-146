# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mtconnect']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mtconnect',
    'version': '0.3.3',
    'description': 'A python agent for MTConnect',
    'long_description': 'None',
    'author': 'Michael Honaker',
    'author_email': 'mchonaker@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
