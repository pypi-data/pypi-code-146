# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['potyk_lib',
 'potyk_lib.dt',
 'potyk_lib.fp',
 'potyk_lib.iter_',
 'potyk_lib.num',
 'potyk_lib.phone']

package_data = \
{'': ['*']}

install_requires = \
['phonenumbers>=8.13.0,<9.0.0', 'python-dateutil>=2.8.2,<3.0.0']

setup_kwargs = {
    'name': 'potyk-lib',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'potykion',
    'author_email': 'potykion@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
