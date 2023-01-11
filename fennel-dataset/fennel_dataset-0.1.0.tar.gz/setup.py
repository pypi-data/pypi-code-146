# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fennel_dataset']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'fennel-dataset',
    'version': '0.1.0',
    'description': 'Empty library from fennel_dataset for Github Actions',
    'long_description': None,
    'author': 'Aditya Nambiar',
    'author_email': 'adityanambiar@fennel.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
