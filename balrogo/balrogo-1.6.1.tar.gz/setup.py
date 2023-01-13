# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['balrogo']

package_data = \
{'': ['*']}

install_requires = \
['astropy>=5.0,<6.0',
 'emcee>=3.0.2,<4.0.0',
 'matplotlib>=3.1.2,<4.0.0',
 'numdifftools>=0.9.39,<0.10.0',
 'numpy>=1.18.5,<2.0.0',
 'scipy>=1.4.1,<2.0.0',
 'shapely>=1.6.4,<2.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=3.3.0,<4.0.0']}

setup_kwargs = {
    'name': 'balrogo',
    'version': '1.6.1',
    'description': 'Bayesian Astrometric Likelihood Recovery of Galactic Objects',
    'long_description': '# BALRoGO\n\n[![pipeline status](https://gitlab.com/eduardo-vitral/balrogo/badges/master/pipeline.svg)](https://gitlab.com/eduardo-vitral/balrogo/-/commits/master)\n[![coverage report](https://gitlab.com/eduardo-vitral/balrogo/badges/master/coverage.svg)](https://gitlab.com/eduardo-vitral/balrogo/-/commits/master)\n[![pypi](https://img.shields.io/pypi/v/balrogo.svg)](https://pypi.python.org/pypi/balrogo/)\n[![python](https://img.shields.io/pypi/pyversions/balrogo.svg)](https://pypi.python.org/pypi/balrogo)\n[![license](http://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)\n\n<!-- markdownlint-disable-next-line no-inline-html -->\n<img alt="logo" align="right" src="https://gitlab.com/eduardo-vitral/balrogo/-/raw/master/logo.png" width="20%" />\n\nBALRoGO: Bayesian Astrometric Likelihood Recovery of Galactic Objects.\n\n- Specially developed to handle data from the Gaia space mission.\n- Extracts galactic objects such as globular clusters and dwarf galaxies from data contaminated by interlopers.\n- Uses a combination of Bayesian and non-Bayesian approaches.\n- Provides:\n  - Fits of proper motion space.\n  - Fits of surface density.\n  - Fits of object center.\n  - Confidence regions for the color-magnitude diagram and parallaxes.\n\nIf something does not work, please [file an issue](https://gitlab.com/eduardo-vitral/balrogo/-/issues).\n\n## Attribution\n\nPlease cite [us](https://academic.oup.com/mnras/article-abstract/504/1/1355/6237524?redirectedFrom=fulltext) if you find this code useful in your research. The BibTeX entry for the paper is:\n\n```bibtex\n@ARTICLE{Vitral21,\n   author = {{Vitral}, Eduardo},\n    title = "BALRoGO: Bayesian Astrometric Likelihood Recovery of Galactic Objects - Global properties of over one hundred globular clusters with Gaia EDR3",\n  journal = {\\mnras},\n     year = 2021,\n    month = jun,\n   volume = {504},\n   number = {1},\n    pages = {1355-1369},\n      doi = {10.1093/mnras/stab947},\n   eprint = {2102.04841},\n   adsurl = {https://ui.adsabs.harvard.edu/abs/2021MNRAS.504.1355V},\n}\n```\n\n## Quick overview\n\nBALRoGO has nine modules that perform different tasks:\n\n- ***angle.py*** : This module contains the main functions concerning angular tansformations, sky projections and spherical trigonomtry.\n- ***gaia.py*** : This module contains the main functions concerning the handling of the Gaia mission data.\n- ***hrd.py*** : This module contains the main functions concerning the color magnitude diagram (CMD). It provides a Kernel Density Estimation (KDE) of the CMD distribution.\n- ***marginals.py*** : This module is based on the Python corner package (Copyright 2013-2016 Dan Foreman-Mackey & contributors, The Journal of Open Source Software): https://joss.theoj.org/papers/10.21105/joss.00024\nI have done some modifications on it so it allows some new features and so it takes into account some choices as default. I thank Gary Mamon for his good suggestions concerning the plot visualization.\n-  ***parallax.py*** : This module contains the main functions concerning parallax information. It provides a kernel density estimation of the distance distribution, as well as a fit of the mode of this distribution.\n- ***pm.py*** : This module contains the main functions concerning proper motion data. It provides MCMC and maximum likelihood fits of proper motions data, as well as robust initial guesses for those fits.\n- ***position.py*** : This module contains the main functions concerning positional information. It provides MCMC and maximum likelihood fits of surface density, as well as robust initial guesses for the (RA,Dec) center of the source.\n- ***mock.py*** : This module handles mock data sets. It converts 3D coordinates to sky coordinates and is able to add realistic errors to proper motions. It is also able to generate Milky Way interlopers.\n- ***dynamics.py*** : This module handles conversions from celestial coordinates to plane of sky coordinates (vPOSr,vPOSt), as well as allows computation of dispersion profiles in different ways. Also computes the velocity anisotropy from cartesian data.\n\n## Installation\n\nBALRoGO is available through [pip](https://pypi.org/project/balrogo/). The quickiest way to install it is to type the following command in your terminal:\n\n```terminal\npip install balrogo\n```\n\nIf you are using [Anaconda](https://www.anaconda.com/), you might want to install it directly in your Anaconda bin path:\n\n```terminal\ncd path/anaconda3/bin/\npip install balrogo\n```\n\nFor updated versions of the code, you can do the same as above, but instead of using `pip install balrogo`, you should type:\n\n```terminal\npip install --upgrade balrogo\n```\n\n### Using BALRoGO on [*Gaia*](https://www.cosmos.esa.int/web/gaia/data-access) data\n\nFor quick tutorial of BALRoGO applied to *Gaia* data, please click [here](https://gitlab.com/eduardo-vitral/balrogo/-/blob/master/GAIA.md).\n\n## License\n\nCopyright (c) 2020 Eduardo Vitral & Alexandre Macedo.\n\nBALRoGO is free software made available under the [MIT License](LICENSE). The BALRoGO logo is licensed under a [Creative Commons Attribution 4.0 International license](https://creativecommons.org/licenses/by/4.0/).\n',
    'author': 'Eduardo Vitral',
    'author_email': 'vitral@iap.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/eduardo-vitral/balrogo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
