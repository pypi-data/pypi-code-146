# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fast_poibin']

package_data = \
{'': ['*']}

install_requires = \
['numba>=0.56.0,<0.57.0', 'numpy>=1.23.0,<2.0.0']

setup_kwargs = {
    'name': 'fast-poibin',
    'version': '0.2.2',
    'description': 'Package for computing PMF and CDF of Poisson binomial distribution.',
    'long_description': "# fast-poibin\n\n[![Build Status](https://github.com/privet-kitty/fast-poibin/workflows/CI/badge.svg)](https://github.com/privet-kitty/fast-poibin/actions)\n[![Coverage Status](https://coveralls.io/repos/github/privet-kitty/fast-poibin/badge.svg?branch=main)](https://coveralls.io/github/privet-kitty/fast-poibin?branch=main)\n\n_This repository is still in alpha stage._\n\nfast-poibin is a Python package for efficiently computing PMF or CDF of Poisson binomial distribution.\n\n\n- Documentation: https://privet-kitty.github.io/fast-poibin/\n- Repository: https://github.com/privet-kitty/fast-poibin/\n\n\n## Dependencies\n\nYou need Python version 3.8.1 or later. As of this writing, Python 3.11.x isn't supported, but it will be available as soon as [numba supports it](https://github.com/numba/numba/issues/8304).\n\n\n## Copyright\n\nCopyright (c) 2023 Hugo Sansaqua.\n",
    'author': 'Hugo Sansaqua',
    'author_email': 'privet.kitty99@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
