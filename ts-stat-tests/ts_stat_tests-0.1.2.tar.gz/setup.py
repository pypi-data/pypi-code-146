# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ts_stat_tests']

package_data = \
{'': ['*']}

install_requires = \
['antropy>=0.1,<0.2',
 'llvmlite>=0.38.1,<0.39.0',
 'numba>=0.55.0,<0.56.0',
 'numpy>=1.21,<1.24',
 'pandas>=1.4,<2.0',
 'pmdarima>=2.0,<3.0',
 'py-tictoc-timer>=1.5,<2.0',
 'scipy>=1.10,<2.0',
 'statsmodels>=0.13,<0.14',
 'tsfeatures>=0.4,<0.5',
 'typeguard>=2.13,<3.0']

setup_kwargs = {
    'name': 'ts-stat-tests',
    'version': '0.1.2',
    'description': 'A suite of statistical tests for time-series data.',
    'long_description': '<div align="center">\n\n# `ts-stat-tests`: Time Series Statistical Tests\n\n<!-- [![pypi](https://img.shields.io/pypi/v/ts-eval)](https://pypi.org/project/ts-eval/) -->\n<!-- [![python3](https://img.shields.io/pypi/pyversions/ts-eval)](https://www.python.org/downloads/release/python-3105/) -->\n[![test suite](https://github.com/chrimaho/ts-stat-tests/actions/workflows/codecov.yml/badge.svg?branch=develop)](https://github.com/chrimaho/ts-stat-tests/actions/workflows/codecov.yml)\n[![codecov](https://codecov.io/gh/chrimaho/ts-stat-tests/branch/main/graph/badge.svg)](https://codecov.io/gh/chrimaho/ts-stat-tests)\n[![docs ci](https://github.com/chrimaho/ts-stat-tests/actions/workflows/docs-ci.yml/badge.svg)](https://github.com/chrimaho/ts-stat-tests/actions/workflows/docs-ci.yml)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![License: MIT](https://img.shields.io/pypi/l/ts-eval)](https://github.com/vshulyak/ts-eval/blob/master/LICENSE)\n[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/chrimaho/ts-stat-tests/issues)\n\n</div>\n\n\n## Motivation\n\nTime Series Analysis has been around for a long time, especially for doing Statistical Testing. Some Python packages are going a long way to make this even easier than it has ever been before. Such as [`sktime`](https://sktime.org/) and [`pycaret`](https://pycaret.org/) and [`pmdarima`](https://www.google.com/search?q=pmdarima) and [`statsmodels`](https://www.statsmodels.org/).\n\nThere are some typical Statistical Tests which are accessible in these Python ([QS](#), [Normality](#), [Stability](#), etc). However, there are still some statistical tests which are not yet ported over to Python, but which have been written in R and are quite stable.\n\nMoreover, there is no one single library package for doing time-series statistical tests in Python.\n\nThat\'s exactly what this package aims to achieve.\n\nA single package for doing all the standard time-series statistical tests.\n\n\n## Tests\n\nFull credit goes to the packages listed in this table.\n\ntype | name | source package | source language | implemented\n---|---|---|---|---\ncorrelation | acf | `statsmodels` | Python | :white_check_mark:\ncorrelation | pacf | `statsmodels` | Python | :white_check_mark:\ncorrelation | ccf | `statsmodels` | Python | :white_check_mark:\nstability | stability | `tsfeatures` | Python | :white_check_mark:\nstability | lumpiness | `tsfeatures` | Python | :white_check_mark:\nsuitability | white-noise (ljung-box) | `` | Python | :white_large_square:\nstationarity | adf | `` | Python | :white_large_square:\nstationarity | kpss | `` | Python | :white_large_square:\nstationarity | ppt | `` | Python | :white_large_square:\nnormality | shapiro | `` | Python | :white_large_square:\nseasonality | qs | `seastests` | R | :white_check_mark:\nseasonality | ocsb | `pmdarima` | Python | :white_check_mark:\nseasonality | ch | `pmdarima` | Python | :white_check_mark:\nseasonality | seasonal strength | `tsfeatures` | Python | :white_check_mark:\nseasonality | trend strength | `tsfeatures` | Python | :white_check_mark:\nseasonality | spikiness | `tsfeatures` | Python | :white_check_mark:\nregularity | regularity | `antropy` | python | :white_check_mark:\n\n\n## Known limitations\n\n- These listed tests is not exhaustive, and there is probably some more that could be added. Therefore, we encourage you to raise issues or pull requests to add more statistical tests to this suite.\n- This package does not re-invent any of these tests. It merely calls the underlying packages, and calls the functions which are already written elsewhere.\n',
    'author': 'Chris Mahoney',
    'author_email': 'chrismahoney@hotmail.com',
    'maintainer': 'Chris Mahoney',
    'maintainer_email': 'chrismahoney@hotmail.com',
    'url': 'https://chrimaho.github.io/ts-stat-tests/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
