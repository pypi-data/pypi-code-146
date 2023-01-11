# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pycalcul']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pycalcul',
    'version': '2.0',
    'description': 'my very first calculator',
    'long_description': '',
    'author': 'LOLpotatoe',
    'author_email': 'victorstefaniusco@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
