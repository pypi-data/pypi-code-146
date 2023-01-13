# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cim',
 'cim.data_profile',
 'cim.loaders',
 'cim.loaders.blazegraph',
 'cim.loaders.gridappsd',
 'cim.loaders.sparql',
 'cim.models']

package_data = \
{'': ['*']}

install_requires = \
['SPARQLWrapper>=2.0.0,<3.0.0',
 'gridappsd-python>=2.2.20220401,<3.0.0',
 'xsdata>=22.5,<23.0']

setup_kwargs = {
    'name': 'gridappsd-cim-profile',
    'version': '0.0.1a3',
    'description': 'CIM models used within gridappsd.',
    'long_description': 'None',
    'author': 'C. Allwardt',
    'author_email': '3979063+craig8@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
