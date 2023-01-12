# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pcmap', 'pcmap.sasa', 'pcmap.sasa.generators']

package_data = \
{'': ['*']}

install_requires = \
['MDAnalysis>=2.3.0,<3.0.0',
 'ccmap>=4.0.2,<5.0.0',
 'docopt>=0.6.2,<0.7.0',
 'ipykernel>=6.20.0,<7.0.0',
 'numpy>=1.19.0,<2.0.0',
 'pypstruct>=0.1.2,<0.2.0',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'pcmap',
    'version': '1.1.4',
    'description': 'Computing contact map for protein structures',
    'long_description': None,
    'author': 'Guillaume Launay',
    'author_email': 'guillaume.launay@ibcp.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MMSB-MOBI/pcmap',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
