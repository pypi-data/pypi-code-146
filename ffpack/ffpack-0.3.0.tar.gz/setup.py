# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ffpack',
 'ffpack.fdr',
 'ffpack.lcc',
 'ffpack.lsg',
 'ffpack.lsm',
 'ffpack.rpm',
 'ffpack.rrm',
 'ffpack.utils']

package_data = \
{'': ['*']}

install_requires = \
['scipy>=1.9,<2.0']

setup_kwargs = {
    'name': 'ffpack',
    'version': '0.3.0',
    'description': 'Fatigue and fracture package',
    'long_description': '# FFPACK - Fatigue and Fracture PACKage\n\n![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/dpzhuX/ffpack/python-package.yml?branch=main)\n![GitHub](https://img.shields.io/github/license/dpzhuX/ffpack)\n[![DOI](https://zenodo.org/badge/575208693.svg)](https://zenodo.org/badge/latestdoi/575208693)\n[![Downloads](https://static.pepy.tech/badge/ffpack)](https://pepy.tech/project/ffpack)\n\n\n## Purpose\n`FFPACK` ( Fatigue and Fracture PACKage ) is an open-source Python library for fatigue and fracture analysis. It supports cycle counting with ASTM methods, load sequence generators, fatigue damage evaluations, etc. A lot of features are under active development. `FFPACK` is designed to help engineers analyze fatigue and fracture behavior in engineering practice.\n\n## Installation\n\n`FFPACK` can be installed via [PyPI](https://pypi.org/project/ffpack/):\n\n```\npip install ffpack\n```\n\n## Status\n\n`FFPACK` is currently under active development. \n\n## Contents\n\n* Fatigue damage rule\n    * Palmgren-miner damage rule\n        * Naive Palmgren-miner damage rule\n        * Classic Palmgren-miner damage rule\n\n* Load correction and counting\n    * ASTM counting\n        * ASTM level crossing counting\n        * ASTM peak counting\n        * ASTM simple range counting\n        * ASTM range pair counting\n        * ASTM rainflow counting\n        * ASTM rainflow counting for repeating history\n    * Johannesson counting\n        * Johannesson min max counting\n    * Rychlik counting\n        * Rychlik rainflow counting\n\n* Load sequence generator\n    * Random walk\n        * Uniform random walk\n    * Autoregressive moving average model\n        * Normal autoregressive (AR) model\n        * Normal moving average (MA) model\n        * Normal ARMA model\n        * Normal ARIMA model\n\n* Load spectra and matrices\n    * Cycle counting matrix\n        * ASTM simple range counting matrix\n        * ASTM range pair counting matrix\n        * ASTM rainflow counting matrix\n        * ASTM rainflow counting matrix for repeating history\n        * Johannesson min max counting matrix\n        * Rychlik rainflow counting matrix\n    * Wave Spectra\n        * Jonswap spectrum\n        * Pierson Moskowitz spectrum\n\n* Random and probabilistic model\n    * Metropolis-Hastings algorithm\n        * Metropolis-Hastings sampler\n    * Nataf algorithm\n        * Nataf transformation\n\n* Risk and reliability model\n    * First order second moment\n        * fosmMVAL\n    * First order reliability method\n        * formHLRF\n        * formCOPT\n\n* Utility methods\n    * Cycle counting aggregation\n    * Counting results to counting matrix\n    * Fitter for SN curve\n    * Sequence peak and valleys\n    * Sequence degitization\n\n## Document\n\nYou can find the latest documentation for setting up `FFPACK` at the [Read the Docs site](https://ffpack.readthedocs.io/en/latest/).\n',
    'author': 'Dongping Zhu',
    'author_email': 'None',
    'maintainer': 'Dongping Zhu',
    'maintainer_email': 'None',
    'url': 'https://pypi.org/project/ffpack',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
