# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pybary']

package_data = \
{'': ['*']}

install_requires = \
['ipykernel>=6.20.1,<7.0.0',
 'ipython>=8.8.0,<9.0.0',
 'jupyter-core>=5.1.2,<6.0.0',
 'matplotlib>=3.6.2,<4.0.0',
 'numpy==1.24.1',
 'seaborn>=0.12.2,<0.13.0']

setup_kwargs = {
    'name': 'pybary',
    'version': '0.1.8',
    'description': 'Barycenter method in python',
    'long_description': '[![Version](https://img.shields.io/pypi/v/pybary.svg)](https://pypi.python.org/pypi/pybary)\n[![python](https://img.shields.io/pypi/pyversions/pybary.svg)](https://pypi.org/project/pybary/)\n[![codecov](https://codecov.io/gh/asmove/pybary/branch/main/graph/badge.svg?token=G8TVJ4X32L)](https://codecov.io/gh/asmove/pybary)\n[![downloads](https://img.shields.io/pypi/dm/pybary)](https://pypi.org/project/pybary/)\n[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/asmove/pybary/HEAD)\n\nPybary\n========\n\n![A sniffer optimizer](https://github.com/asmove/pybary/blob/main/images/pybary-tiny.png?raw=true)\n\nBarycenter method in python. Take a look at original article: https://arxiv.org/abs/1801.10533\n\nHow to install\n----------------\n\nWe run the command on desired installation environment:\n\n``` {.bash}\npip install pybary\n```\n\nMinimal example\n----------------\n\nWe may code examples by performing following actions \n\n1. Run command `python examples/example.py` from package root folder;\n2. Open notebook `examples/example.ipynb` and run cell on given order.\n',
    'author': 'Bruno Peixoto',
    'author_email': 'brunolnetto@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pypi.org/project/pybary/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<3.12',
}


setup(**setup_kwargs)
