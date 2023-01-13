# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['basketix',
 'basketix.entities',
 'basketix.handlers',
 'basketix.helpers',
 'basketix.models',
 'basketix.models.attributes',
 'basketix.tables']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.26.22,<2.0.0',
 'isoweek>=1.3.3,<2.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'pytz>=2022.6,<2023.0',
 'typing-extensions>=4.4.0,<5.0.0']

setup_kwargs = {
    'name': 'basketix',
    'version': '0.1.23',
    'description': '',
    'long_description': '',
    'author': 'tlartigau',
    'author_email': 'thomaslartigau@hotmail.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
