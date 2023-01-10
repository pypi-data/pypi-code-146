# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['parasect']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'click>=8.0.1,<9.0.0',
 'defusedxml>=0.7.1,<0.8.0',
 'directory-tree>=0.0.2,<0.0.3',
 'pydantic>=1.9.1,<2.0.0']

entry_points = \
{'console_scripts': ['parasect = parasect.__main__:cli']}

setup_kwargs = {
    'name': 'parasect',
    'version': '1.1.0',
    'description': 'Utility for manipulating parameter sets for autopilots.',
    'long_description': "Parasect\n========\n\n.. badges-begin\n\n|PyPI| |Status| |Python Version| |License|\n\n|Read the Docs| |Tests| |Codecov|\n\n|pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/parasect.svg\n   :target: https://pypi.org/project/parasect/\n   :alt: PyPI\n.. |Status| image:: https://img.shields.io/pypi/status/parasect.svg\n   :target: https://pypi.org/project/parasect/\n   :alt: Status\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/parasect\n   :target: https://pypi.org/project/parasect\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/github/license/AvyFly/parasect\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/parasect/latest.svg?label=Read%20the%20Docs\n   :target: https://parasect.readthedocs.io/\n   :alt: Read the documentation at https://parasect.readthedocs.io/\n.. |Tests| image:: https://github.com/AvyFly/parasect/workflows/Tests/badge.svg\n   :target: https://github.com/AvyFly/parasect/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/AvyFly/parasect/branch/master/graph/badge.svg\n   :target: https://codecov.io/gh/AvyFly/parasect\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\n.. badges-end\n\n.. image:: docs/_static/logo.svg\n   :alt: parasect logo\n   :width: 320\n   :align: center\n\n.. logo-end\n\n\nWelcome to *Parasect*, a utility for manipulating parameter sets for autopilots!\n\nFeatures\n--------\n\n*Parasect* has two-fold capabilities:\n\n1. Compare two parameter sets and highlighting their differences.\n2. Parsing from user-defined content and generating new parameter sets, ready for loading into an autopilot.\n\nList of currently supported autopilots:\n\n* PX4_\n\nRequirements\n------------\n\n*Parasect* is a pure-Python project. Its requirements are managed by the Poetry_ dependency manager.\nWhen you install *Parasect* via pip_ its requirements will also be installed automatically.\n\nCurrently *Parasect* has been tested:\n\n* in Continuous Integration servers for **Ubuntu Linux**, **Windows**\n* manually in **Ubuntu Linux**.\n\n\nInstallation\n------------\n\nYou can install *Parasect* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install parasect\n\n\nUsage\n-----\n\n*Parasect* is primarily used as a command-line program.\nIn its simplest form, two parameter files can be compared via:\n\n.. code:: console\n\n   $ parasect compare <FILE_1> <FILE_2>\n\nThe usage for building parameter sets is more involved.\nPlease see the `Command-line Reference <CLI usage_>`_ for details.\n\nAdditionally, it exposes a minimal API, enabling automated operations.\nThis is described in the `API Reference <API usage_>`_.\n\nIt is strongly recommended that you read the Concepts_ that *Parasect* employs, if you plan to make full use of it.\n\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the `MIT license`_,\n*Parasect* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\nCredits\n-------\n\nThis project was sponsored by `Avy B.V. <Avy_>`_, a UAV company in Amsterdam.\n\nThis project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.\n\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _MIT license: https://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _file an issue: https://github.com/AvyFly/parasect/issues\n.. _pip: https://pip.pypa.io/\n.. _CLI usage: https://parasect.readthedocs.io/en/latest/reference.html#cli-reference\n.. _API usage: https://parasect.readthedocs.io/en/latest/reference.html#api-reference\n.. _Concepts: https://parasect.readthedocs.io/en/latest/concepts.html\n.. _PX4: https://px4.io/\n.. _Poetry: https://python-poetry.org/\n.. _Avy: https://avy.eu\n.. github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n",
    'author': 'George Zogopoulos',
    'author_email': 'geo.zogop.papal@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/AvyFly/parasect',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
