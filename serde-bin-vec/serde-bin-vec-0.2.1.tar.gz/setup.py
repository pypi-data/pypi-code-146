# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['serde_bin_vec']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'serde-bin-vec',
    'version': '0.2.1',
    'description': 'serde vecs in bin format',
    'long_description': None,
    'author': 'Andrew Matte',
    'author_email': 'andrew.matte@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
