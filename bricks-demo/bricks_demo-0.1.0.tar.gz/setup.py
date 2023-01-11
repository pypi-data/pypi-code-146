# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bricks_demo']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'bricks-demo',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Markel',
    'author_email': 'markel.baskaran@alumni.mondragon.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
