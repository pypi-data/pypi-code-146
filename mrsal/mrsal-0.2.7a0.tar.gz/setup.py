# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mrsal', 'mrsal.config']

package_data = \
{'': ['*']}

install_requires = \
['colorlog>=6.7.0,<7.0.0', 'pika>=1.3.0,<2.0.0', 'retry>=0.9.2,<0.10.0']

setup_kwargs = {
    'name': 'mrsal',
    'version': '0.2.7a0',
    'description': '',
    'long_description': 'None',
    'author': 'Raafat',
    'author_email': 'rafatzahran90@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
