# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['orcpy', 'orcpy.design']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'orcpy',
    'version': '0.1.0',
    'description': 'A python package for designing organic Rankine cycles',
    'long_description': '',
    'author': 'Mehran Ahmadpour',
    'author_email': 'mehran.hmdpr@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
