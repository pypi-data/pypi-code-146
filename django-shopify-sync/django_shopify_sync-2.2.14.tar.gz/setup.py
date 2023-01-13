# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shopify_sync',
 'shopify_sync.migrations',
 'shopify_sync.models',
 'shopify_sync.tests']

package_data = \
{'': ['*'], 'shopify_sync.tests': ['fixtures/*']}

install_requires = \
['ShopifyAPI>=12.2.0',
 'django-shopify-webhook>=0.2.6',
 'django>=2.2',
 'jsonfield>=0.9.22']

setup_kwargs = {
    'name': 'django-shopify-sync',
    'version': '2.2.14',
    'description': 'A package for synchronising Django models with Shopify resources.',
    'long_description': 'None',
    'author': 'David Burke',
    'author_email': 'dburke@thelabnyc.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/thelabnyc/django-shopify-sync',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
