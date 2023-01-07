# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openweatherclass']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.4,<2.0.0', 'requests==2.28.1']

setup_kwargs = {
    'name': 'openweatherclass',
    'version': '0.5.0',
    'description': 'An implementation of the Openweather API in Python.',
    'long_description': 'None',
    'author': 'Brian Hudson',
    'author_email': 'reallybrianhudson@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
