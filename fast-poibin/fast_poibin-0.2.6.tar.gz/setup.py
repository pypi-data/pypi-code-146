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
    'version': '0.2.6',
    'description': 'Package for computing PMF and CDF of Poisson binomial distribution.',
    'long_description': "# fast-poibin\n\n[![Build Status](https://github.com/privet-kitty/fast-poibin/workflows/CI/badge.svg)](https://github.com/privet-kitty/fast-poibin/actions)\n[![Coverage Status](https://coveralls.io/repos/github/privet-kitty/fast-poibin/badge.svg?branch=main)](https://coveralls.io/github/privet-kitty/fast-poibin?branch=main)\n[![PyPI Version](https://img.shields.io/pypi/v/fast-poibin)](https://pypi.org/project/fast-poibin/)\n\n\nfast-poibin is a Python package for efficiently computing PMF or CDF of Poisson binomial distribution.\n\n\n- API Reference: https://privet-kitty.github.io/fast-poibin/\n- Repository: https://github.com/privet-kitty/fast-poibin/\n\n\n## Installation\n\n\n\n```bash\npip install fast-poibin\n```\n\n\nYou need Python version 3.8 or later. As of this writing, Python 3.11 isn't supported, but it will be available as soon as [numba supports it](https://github.com/numba/numba/issues/8304).\n\n## Basic Usage\n\n\n```python\n>>> from fast_poibin import PoiBin\n>>> poibin = PoiBin([0.1, 0.2, 0.2])\n>>> poibin.pmf\narray([0.576, 0.352, 0.068, 0.004])\n>>> poibin.cdf\narray([0.576, 0.928, 0.996, 1.   ])\n```\n\n\n\n\n## Copyright\n\nCopyright (c) 2023 Hugo Sansaqua.\n",
    'author': 'Hugo Sansaqua',
    'author_email': 'privet.kitty99@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/privet-kitty/fast-poibin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
