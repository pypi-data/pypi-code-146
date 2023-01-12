# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ayaka', 'ayaka.adapters']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ayaka',
    'version': '0.0.0.0b3',
    'description': '猫猫，猫猫！',
    'long_description': '<div align="center">\n\n# Ayaka - 猫猫，猫猫！ - 0.0.0.0b3\n\n</div>\n',
    'author': 'Su',
    'author_email': 'wxlxy316@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://bridgel.github.io/ayaka/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
