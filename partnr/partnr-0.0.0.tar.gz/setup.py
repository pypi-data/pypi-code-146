# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['partnr']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'partnr',
    'version': '0.0.0',
    'description': 'PARTNR learns to solve ambiguities in pick and place problems through interactive learning.s',
    'long_description': 'None',
    'author': 'Jelle Luijkx',
    'author_email': 'j.d.luijkx@tudelft.nl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://partnr-learn.github.io',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
