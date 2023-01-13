# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['m2stitch']

package_data = \
{'': ['*']}

install_requires = \
['click>=7,<9',
 'networkx>=2.5.1,<3.0.0',
 'numpy>=1.22,<2.0',
 'pandas-stubs>=1.2.0,<1.3',
 'pandas>=1.2.4,<2.0.0',
 'scikit-learn>=1.0.2,<2.0.0',
 'scipy>=1.6.3,<2.0.0',
 'tqdm>=4.60.0,<5.0.0']

entry_points = \
{'console_scripts': ['m2stitch = m2stitch.__main__:main']}

setup_kwargs = {
    'name': 'm2stitch',
    'version': '0.7.0',
    'description': 'M2Stitch',
    'long_description': "M2Stitch\n========\n\n|PyPI| |Python Version| |License|\n\n|Read the Docs| |Tests| |Codecov|\n\n|pre-commit| |Black| |Zenodo|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/m2stitch.svg\n   :target: https://pypi.org/project/m2stitch/\n   :alt: PyPI\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/m2stitch\n   :target: https://pypi.org/project/m2stitch\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/m2stitch\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/m2stitch/latest.svg?label=Read%20the%20Docs\n   :target: https://m2stitch.readthedocs.io/\n   :alt: Read the documentation at https://m2stitch.readthedocs.io/\n.. |Tests| image:: https://github.com/yfukai/m2stitch/workflows/Tests/badge.svg\n   :target: https://github.com/yfukai/m2stitch/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/yfukai/m2stitch/branch/master/graph/badge.svg\n   :target: https://codecov.io/gh/yfukai/m2stitch\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n.. |Zenodo| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.5139597.svg\n   :target: https://doi.org/10.5281/zenodo.5139597\n   :alt: Zenodo\n\nFeatures\n--------\n\n- Provides robust stitching of tiled microscope images on a regular grid, mostly following algorithm by MIST_ but improved in several points.\n- Supports missing tiles.\n\nInstallation\n------------\n\nYou can install *M2Stitch* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install m2stitch\n\n\nUsage\n-----\n\nPlease see the Usage_ for details.\n\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the `MIT license`_,\n*M2Stitch* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\nCredits\n-------\n\nThis program is an unofficial implementation of MIST_ stitching algorithm on GitHub_. The original paper is here_.\n\nThis project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.\n\n.. _MIST: https://pages.nist.gov/MIST\n.. _GitHub: https://github.com/usnistgov/MIST\n.. _here: https://github.com/USNISTGOV/MIST/wiki/assets/mist-algorithm-documentation.pdf\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _MIT license: https://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _file an issue: https://github.com/yfukai/m2stitch/issues\n.. _pip: https://pip.pypa.io/\n.. github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n.. _Usage: https://m2stitch.readthedocs.io/en/latest/usage.html\n\nOther Python stitching programs\n-------------------------------\nOne might also be interested in another Python-written stitching tool\nASHLAR_ (bioRxiv_),\nwith a comparable performance to that of MIST and additional features.\n\n.. _ASHLAR: https://github.com/labsyspharm/ashlar\n.. _bioRxiv: https://www.biorxiv.org/content/10.1101/2021.04.20.440625v1\n",
    'author': 'Yohsuke Fukai',
    'author_email': 'ysk@yfukai.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/yfukai/m2stitch',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
