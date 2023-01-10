# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sw_product_lib', 'sw_product_lib.client', 'sw_product_lib.errors']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.8.0,<0.9.0',
 'fastapi>=0.85.0,<0.86.0',
 'gql[all]>=3.3.0,<4.0.0',
 'python-jose[cryptography]>=3.3.0,<4.0.0',
 'rich>=12.4.4,<13.0.0',
 'sgqlc>=16.0,<17.0']

setup_kwargs = {
    'name': 'sw-product-lib',
    'version': '0.3.0',
    'description': 'Python library for Strangeworks products to interact with the Strangeworks Platform',
    'long_description': 'None',
    'author': 'Strangeworks Devs',
    'author_email': 'hello@strangeworks.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
