# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['timewise']

package_data = \
{'': ['*']}

install_requires = \
['astropy>=5.1,<6.0',
 'backoff>=2.1.2,<3.0.0',
 'coveralls>=3.3.1,<4.0.0',
 'furo>=2022.6.21,<2023.0.0',
 'matplotlib>=3.5.3,<4.0.0',
 'myst-parser>=0.18.0,<0.19.0',
 'numpy>=1.23.2,<2.0.0',
 'pandas>=1.4.3,<2.0.0',
 'pyvo>=1.3,<2.0',
 'requests>=2.28.1,<3.0.0',
 'scikit-image>=0.19.3,<0.20.0',
 'seaborn>=0.11.2,<0.13.0',
 'tqdm>=4.64.0,<5.0.0',
 'virtualenv>=20.16.3,<21.0.0']

setup_kwargs = {
    'name': 'timewise',
    'version': '0.3.0rc5',
    'description': 'A small package to download infrared data from the WISE satellite',
    'long_description': "[![CI](https://github.com/JannisNe/timewise/actions/workflows/continous_integration.yml/badge.svg)](https://github.com/JannisNe/timewise/actions/workflows/continous_integration.yml)\n[![Coverage Status](https://coveralls.io/repos/github/JannisNe/timewise/badge.svg?branch=main)](https://coveralls.io/github/JannisNe/timewise?branch=main)\n[![PyPI version](https://badge.fury.io/py/timewise.svg)](https://badge.fury.io/py/timewise)\n[![Documentation Status](https://readthedocs.org/projects/timewise/badge/?version=latest)](https://timewise.readthedocs.io/en/latest/?badge=latest)\n[![DOI](https://zenodo.org/badge/449677569.svg)](https://zenodo.org/badge/latestdoi/449677569)\n\n\n\n# `timewise` is great, love it!\nDownload infrared lightcurves recorded with the WISE satellite.\n\n## Installation\n\n`timewise` is a python package, installable through `pip`\n```\npip install timewise\n```\n\nIf you would like to contribute just clone the repository. Easy.\n\n\n## Dependencies\n\nAll dependencies are listed in `requirements.txt`. If installing with `pip` they will automatically installed.\nOtherwise you can install them with `pip install -r requirements.txt`.\n\nThere is one package that does not obey! It's `SciServer`! \nIt's used to access SDSS data and plot cutouts. If you want to use this functionality \ninstall [this](https://github.com/sciserver/SciScript-Python) and create an account [here](https://www.sciserver.org).\nAs soon as required you will be required to enter your username and password.\n\n\n## Testing\n You can verify that everything is working (because this package is flawless and works everywhere.) by executing\n the unittest\n```\npython -m unittest discover tests/\n```\n\n## Cite\nIf you you `timewise` please cite [this](https://zenodo.org/badge/latestdoi/449677569).\n\n## Usage\nDetailed documentation can be found [here](https://timewise.readthedocs.io/en/latest/)\n",
    'author': 'Jannis Necker',
    'author_email': 'jannis.necker@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/JannisNe/timewise',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
