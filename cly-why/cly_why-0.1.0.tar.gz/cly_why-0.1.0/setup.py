# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cly_why']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cly-why',
    'version': '0.1.0',
    'description': 'A super simple functional cli helper lib',
    'long_description': '',
    'author': '00il',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
