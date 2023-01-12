# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['convnets']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'convnets',
    'version': '0.1.0',
    'description': 'Convolutional Neural Networks and utilities for Computer Vision',
    'long_description': '# convnets\n\nConvolutional Neural Networks and utilities for Computer Vision.\n',
    'author': 'juansensio',
    'author_email': 'sensio.juan@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
