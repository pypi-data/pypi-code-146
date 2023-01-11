# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ivyorm',
 'ivyorm.module',
 'ivyorm.module.connection',
 'ivyorm.module.interface',
 'ivyorm.module.util']

package_data = \
{'': ['*'], 'ivyorm': ['ivypy.egg-info/*', 'model/*']}

setup_kwargs = {
    'name': 'ivyorm',
    'version': '0.1.16',
    'description': 'An ORM for Python',
    'long_description': "Ivy ORM allows you to write data access instructions that are then converted to the database you are working with.\n\nBy providing a schema file to the Datasource class, you are able to (hopefully) quickly write some code that allows you to query a database\n\n# Current status\nThis is a very 'alpha' build. I've only done the very basics such as create and drop tables, and CRUD operations.\nThere is also only one connector - Postgres!",
    'author': 'James Randell',
    'author_email': 'jamesrandell@me.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
