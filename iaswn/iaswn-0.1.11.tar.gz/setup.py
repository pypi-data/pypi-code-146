# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iaswn']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'iaswn',
    'version': '0.1.11',
    'description': '(GPLv3/Python 3.9+) Python object <-> JSON string',
    'long_description': 'None',
    'author': 'suizokukan',
    'author_email': 'suizokukan@orange.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
