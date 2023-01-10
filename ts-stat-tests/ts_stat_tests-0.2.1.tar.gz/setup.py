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
    'version': '0.2.1',
    'description': 'A suite of statistical tests for time-series data.',
    'long_description': '<div align="center">\n\n# Time Series Statistical Tests\n\n### `ts-stat-tests`\n\n[![PyPI version](https://img.shields.io/pypi/v/ts-stat-tests?label=version&logo=git&color=blue)](https://pypi.org/project/ts-stat-tests/)\n[![Python](https://img.shields.io/pypi/pyversions/ts-stat-tests.svg?style=flat&logo=python&logoColor=FFDE50&color=blue)](https://pypi.org/project/ts-stat-tests/)\n[![OS](https://img.shields.io/static/v1?label=os&message=ubuntu+|+macos+|+windows&color=blue&logo=ubuntu&logoColor=green)](https://pypi.org/project/ts-stat-tests/)<br>\n[![Unit Tests](https://img.shields.io/github/actions/workflow/status/chrimaho/ts-stat-tests/ci-unit-tests.yml?logo=github&logoColor=white&label=unit+tests)](https://github.com/chrimaho/ts-stat-tests/actions/workflows/ci-unit-tests.yml)\n[![Deploy Docs](https://img.shields.io/github/actions/workflow/status/chrimaho/ts-stat-tests/cd-deploy-docs.yml?logo=github&logoColor=white&label=deploy+docs)](https://github.com/chrimaho/ts-stat-tests/actions/workflows/cd-deploy-docs.yml)\n[![Publish Package](https://img.shields.io/github/actions/workflow/status/chrimaho/ts-stat-tests/cd-publish-package.yml?logo=github&logoColor=white&label=publish+package)](https://github.com/chrimaho/ts-stat-tests/actions/workflows/cd-publish-package.yml)\n[![codecov](https://codecov.io/gh/chrimaho/ts-stat-tests/branch/main/graph/badge.svg)](https://codecov.io/gh/chrimaho/ts-stat-tests)<br>\n[![Vulnerabilities](https://img.shields.io/snyk/vulnerabilities/github/chrimaho/ts-stat-tests?color=green)](https://github.com/chrimaho/ts-stat-tests)\n[![License MIT](https://img.shields.io/pypi/l/ts-stat-tests)](https://github.com/chrimaho/ts-stat-tests/blob/master/LICENSE)\n[![Downloads](https://img.shields.io/pypi/dw/ts-stat-tests)](https://github.com/chrimaho/ts-stat-tests)\n[![Code style: black](https://img.shields.io/badge/code_style-black-000000.svg)](https://github.com/psf/black)<br>\n[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/chrimaho/ts-stat-tests/issues)\n\n</div>\n\n\n## Motivation\n\nTime Series Analysis has been around for a long time, especially for doing Statistical Testing. Some Python packages are going a long way to make this even easier than it has ever been before. Such as [`sktime`](https://sktime.org/) and [`pycaret`](https://pycaret.org/) and [`pmdarima`](https://www.google.com/search?q=pmdarima) and [`statsmodels`](https://www.statsmodels.org/).\n\nThere are some typical Statistical Tests which are accessible in these Python ([QS](#), [Normality](#), [Stability](#), etc). However, there are still some statistical tests which are not yet ported over to Python, but which have been written in R and are quite stable.\n\nMoreover, there is no one single library package for doing time-series statistical tests in Python.\n\nThat\'s exactly what this package aims to achieve.\n\nA single package for doing all the standard time-series statistical tests.\n\n\n## Tests\n\nFull credit goes to the packages listed in this table.\n\ntype | name | source package | source language | implemented\n---|---|---|---|---\ncorrelation | acf | `statsmodels` | Python | ✅\ncorrelation | pacf | `statsmodels` | Python | ✅\ncorrelation | ccf | `statsmodels` | Python | ✅\nstability | stability | `tsfeatures` | Python | ✅\nstability | lumpiness | `tsfeatures` | Python | ✅\nsuitability | white-noise (ljung-box) | ` ` | Python | 🔲\nstationarity | adf | ` ` | Python | 🔲\nstationarity | kpss | ` ` | Python | 🔲\nstationarity | ppt | ` ` | Python | 🔲\nnormality | shapiro | ` ` | Python | 🔲\nseasonality | qs | `seastests` | R | ✅\nseasonality | ocsb | `pmdarima` | Python | ✅\nseasonality | ch | `pmdarima` | Python | ✅\nseasonality | seasonal strength | `tsfeatures` | Python | ✅\nseasonality | trend strength | `tsfeatures` | Python | ✅\nseasonality | spikiness | `tsfeatures` | Python | ✅\nregularity | regularity | `antropy` | python | ✅\n\n\n## Known limitations\n\n- These listed tests is not exhaustive, and there is probably some more that could be added. Therefore, we encourage you to raise issues or pull requests to add more statistical tests to this suite.\n- This package does not re-invent any of these tests. It merely calls the underlying packages, and calls the functions which are already written elsewhere.\n',
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
