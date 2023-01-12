# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rex', 'rex.proto']

package_data = \
{'': ['*']}

install_requires = \
['flax>=0.6.3,<0.7.0',
 'gym>=0.21.0,<0.22.0',
 'jax-jumpy>=0.2.0,<0.3.0',
 'jax>=0.4.1,<0.5.0',
 'matplotlib>=3.6.2,<4.0.0',
 'networkx>=2.8.8,<3.0.0',
 'protobuf>=3.20,<4.0',
 'seaborn>=0.12.1,<0.13.0',
 'tensorflow-probability>=0.19.0,<0.20.0',
 'termcolor>=2.1.1,<3.0.0']

setup_kwargs = {
    'name': 'rex-lib',
    'version': '0.0.1',
    'description': 'Rex is a tool for creating Robotic Environments with jaX.',
    'long_description': None,
    'author': 'Bas van der Heijden',
    'author_email': 'd.s.vanderheijden@tudelft.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bheijden/rex',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
