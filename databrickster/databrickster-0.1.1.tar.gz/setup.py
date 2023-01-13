# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['databrickster']

package_data = \
{'': ['*'], 'databrickster': ['.pytest_cache/*', '.pytest_cache/v/cache/*']}

setup_kwargs = {
    'name': 'databrickster',
    'version': '0.1.1',
    'description': '',
    'long_description': '',
    'author': 'Hubert Dudek',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
