# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ciclo']

package_data = \
{'': ['*']}

install_requires = \
['einop>=0.0.1',
 'flax>=0.6.0',
 'jax>=0.3.0',
 'jaxlib>=0.3.0',
 'pkbar>=0.5',
 'tqdm>=4.0.0']

setup_kwargs = {
    'name': 'ciclo',
    'version': '0.1.6',
    'description': '',
    'long_description': 'None',
    'author': 'Cristian Garcia',
    'author_email': 'cgarcia.e88@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
