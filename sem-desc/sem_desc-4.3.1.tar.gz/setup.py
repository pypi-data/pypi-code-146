# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sm', 'sm.evaluation', 'sm.inputs', 'sm.misc', 'sm.namespaces', 'sm.outputs']

package_data = \
{'': ['*'], 'sm': ['data/*']}

install_requires = \
['Deprecated>=1.2.13,<2.0.0',
 'colorama>=0.4.4',
 'graph-wrapper>=1.5.0,<2.0.0',
 'ipython>=8.0.1,<9.0.0',
 'loguru>=0.6.0,<0.7.0',
 'matplotlib>=3.5.3,<4.0.0',
 'orjson>=3.8.2,<4.0.0',
 'pandas>=1.4.1,<2.0.0',
 'pydot>=1.4.2,<2.0.0',
 'pyrsistent>=0.17.3,<0.18.0',
 'python-slugify>=6.1.2,<7.0.0',
 'ray>=2.0.1,<3.0.0',
 'rdflib>=6.1.1,<7.0.0',
 'rsoup>=2.5.1,<3.0.0',
 'ruamel.yaml>=0.17.21,<0.18.0',
 'serde2[all]>=1.5.0,<2.0.0',
 'timer4>=1.0.2,<2.0.0',
 'tqdm>=4.64.0,<5.0.0',
 'ujson>=5.5.0,<6.0.0']

setup_kwargs = {
    'name': 'sem-desc',
    'version': '4.3.1',
    'description': 'Package providing basic functionalities for the semantic modeling problem',
    'long_description': '# SEM-DESC ![PyPI](https://img.shields.io/pypi/v/sem-desc)\n\nContaining basic functions (input, output, dataset, evaluation metrics) for the semantic modeling problem.\n',
    'author': 'Binh Vu',
    'author_email': 'binh@toan2.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/binh-vu/sm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
