# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['smolke_data',
 'smolke_data.common',
 'smolke_data.common.utils',
 'smolke_data.common.validator']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'smolke-data',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Smolke',
    'author_email': 'd.smolczynski1@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
