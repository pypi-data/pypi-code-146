# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ussa1976']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0',
 'netCDF4>=1.5.7',
 'numpy>=1.22',
 'scipy>=1.6.3',
 'xarray>=0.18.2']

entry_points = \
{'console_scripts': ['ussa1976 = ussa1976.__main__:main']}

setup_kwargs = {
    'name': 'ussa1976',
    'version': '0.3.3',
    'description': 'The U.S. Standard Atmosphere 1976 model.',
    'long_description': "USSA1976\n========\n\n*The U.S. Standard Atmosphere 1976 model.*\n\n|PyPI| |Python Version| |License|\n\n|Read the Docs| |Tests| |Codecov|\n\n|pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/ussa1976.svg\n   :target: https://pypi.org/project/ussa1976/\n   :alt: PyPI\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/ussa1976\n   :target: https://pypi.org/project/ussa1976\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/ussa1976\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/ussa1976/latest.svg?label=Read%20the%20Docs\n   :target: https://ussa1976.readthedocs.io/\n   :alt: Read the documentation at https://ussa1976.readthedocs.io/\n.. |Tests| image:: https://github.com/nollety/ussa1976/workflows/Tests/badge.svg\n   :target: https://github.com/nollety/ussa1976/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/nollety/ussa1976/branch/main/graph/badge.svg\n   :target: https://codecov.io/gh/nollety/ussa1976\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\nThis package implements the atmosphere thermophysical model provided by the\nNational Aeronautics and Space Administration technical report NASA-TM-X-74335\npublished in 1976 and entitled *U.S. Standard Atmosphere, 1976*.\n\nFeatures\n--------\n\n* Run the U.S. Standard Atmosphere 1976 model on your custom altitude grid\n* Compute all 14 atmospheric variables of the model as a function of altitude:\n   * air temperature\n   * air pressure\n   * number density (of individual species)\n   * air number density\n   * air density\n   * air molar volume\n   * air pressure scale height\n   * air particles mean speed\n   * air particles mean free path\n   * air particles mean collision frequency\n   * speed of sound in air\n   * air dynamic viscosity\n   * air kinematic viscosity\n   * air thermal conductivity coefficient\n* Results stored in `NetCDF <https://www.unidata.ucar.edu/software/netcdf/>`_\n  format\n* Command-line interface\n* Python interface\n\n\nRequirements\n------------\n\n* Python 3.8+\n\n\nInstallation\n------------\n\nYou can install *USSA1976* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install ussa1976\n\n\nUsage\n-----\n\n* For the Command-line interface, please see the\n  `Command-line Reference <Usage_>`_ for details.\n* For the Python interface, refer to the `User Guide <_user_guide>`_.\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the `MIT license`_,\n*USSA1976* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\nCredits\n-------\n\nThis project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.\n\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _MIT license: https://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _file an issue: https://github.com/nollety/ussa1976/issues\n.. _pip: https://pip.pypa.io/\n.. github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n.. _Usage: https://ussa1976.readthedocs.io/en/latest/usage.html\n",
    'author': 'Yvan Nollet',
    'author_email': 'yvan.nollet@rayference.eu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/nollety/ussa1976',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
