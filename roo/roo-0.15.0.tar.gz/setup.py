# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['roo',
 'roo.caches',
 'roo.cli',
 'roo.cli.add',
 'roo.cli.cache',
 'roo.cli.environment',
 'roo.cli.export',
 'roo.cli.init',
 'roo.cli.install',
 'roo.cli.lock',
 'roo.cli.package',
 'roo.cli.rswitch',
 'roo.cli.run',
 'roo.deptree',
 'roo.exporters',
 'roo.exporters.lock',
 'roo.files',
 'roo.parsers',
 'roo.semver',
 'roo.sources']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.13,<4.0.0',
 'atomicwrites>=1.4,<2.0',
 'beautifulsoup4>=4.8.2,<5.0.0',
 'click>=7.0,<8.0',
 'packaging>=20.1,<21.0',
 'requests>=2.22.0,<3.0.0',
 'rich>=11.0.0,<12.0.0',
 'toml>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['roo = roo.cli.__main__:main']}

setup_kwargs = {
    'name': 'roo',
    'version': '0.15.0',
    'description': 'A package manager to handle R environments',
    'long_description': '# Roo - manages environments and dependencies in R\n\n![Build](https://github.com/AstraZeneca/roo/actions/workflows/python.yml/badge.svg)\n![Flake8](https://github.com/AstraZeneca/roo/actions/workflows/lint.yml/badge.svg)\n[![Maturity Level](https://img.shields.io/badge/Maturity%20Level-Under%20Development-orange)](https://img.shields.io/badge/Maturity%20Level-Under%20Development-orange)\n\n# Description\n\nRoo is a python program that handles R dependencies and R environments, ensuring environment reproducibility\nthat satisfy dependency constraints. If you are familiar with python poetry or pip it aims at being the same.\n\n## Motivation\n\nRoo was born out of frustration at the current R environment handling tools\nthat are not up to expected needs when it\'s time to ensure a reproducible\nenvironment that is guaranteed to have dependencies satisfied. Utilities such\nas packrat and renv, and the general status of CRAN, do not favour such\nreliability. \n\nMost R programmers always use the most recent code available on CRAN, but this\nis not going to work for validated applications that need a specified environment\nthat is unchanged even if a reinstallation happens at a later date. While you could\nargue that packrat or renv freezes the packages in the current environment,\nunfortunately the mechanism with which those packages are discovered to begin\nwith has potential issues.\n\n### Subdependency conflicts, and why it\'s a problem\n\nSay for example that you want to install two packages, `A` and `B`. Both depend on\npackage `C`.  However, `A` depends on `C >= 2`, and `B` depends on `C < 2`. \n\nIt is obvious that there is no version of `C` that satisfies the constraints,\ntherefore the environment cannot be created. This is an important point that\none wants to be aware of, because validation depends on a reliable and\nconsistent environment.\n\nThere are effective techniques to deal with this so called "dependency hell".\nRoo is not as performant as tools such as conda and poetry for python, but it\nsatisfies the basic need I currently have to ensure the environment is stable,\nreproducible, and consistent (of course, assuming that the annotations in the\npackages are correct!)\n\nRoo does a lot more than this, and it\'s basically a work in progress. As a data\nscientist you are unlikely to need Roo in your daily work, because Roo is\nmostly focused on production-level rather than exploratory coding. However, if time\nallows, an R interface will be written to at least install from a roo lock file.\n\n# Requirements and Installation\n\nRoo is written in python and requires python 3.8 or above. \nIt runs on any platform, and it can be installed from pypi with:\n\n    pip install roo\n\nDependencies will be installed automatically.\n',
    'author': 'Stefano Borini',
    'author_email': 'stefano.borini@astrazeneca.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AstraZeneca/roo',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
