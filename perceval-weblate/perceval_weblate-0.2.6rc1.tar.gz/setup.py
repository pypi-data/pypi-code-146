# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['perceval', 'perceval.backends.weblate', 'tests']

package_data = \
{'': ['*'], 'tests': ['data/weblate/*']}

install_requires = \
['grimoirelab-toolkit>=0.3', 'perceval>=0.19', 'requests>=2.7.0,<3.0.0']

setup_kwargs = {
    'name': 'perceval-weblate',
    'version': '0.2.6rc1',
    'description': 'Bundle of Perceval backends for Weblate.',
    'long_description': '# perceval-weblate [![Build Status](https://github.com/chaoss/grimoirelab-perceval-weblate/workflows/tests/badge.svg)](https://github.com/chaoss/grimoirelab-perceval-weblate/actions?query=workflow:tests+branch:master+event:push) [![Coverage Status](https://img.shields.io/coveralls/chaoss/grimoirelab-perceval-weblate.svg)](https://coveralls.io/r/chaoss/grimoirelab-perceval-weblate?branch=master) [![PyPI version](https://badge.fury.io/py/perceval-weblate.svg)](https://badge.fury.io/py/perceval-weblate)\n\nBundle of Perceval backends for Weblate.\n\n## Backends\n\nThe backends currently managed by this package support the next repositories:\n\n* Weblate\n\n## Requirements\n\n * Python >= 3.7\n\nYou will also need some other libraries for running the tool, you can find the\nwhole list of dependencies in [pyproject.toml](pyproject.toml) file.\n\n## Installation\n\nThere are several ways to install perceval-weblate on your system: packages or source \ncode using Poetry or pip.\n\n### PyPI\n\nperceval-weblate can be installed using pip, a tool for installing Python packages. \nTo do it, run the next command:\n```\n$ pip install perceval-weblate\n```\n\n### Source code\n\nTo install from the source code you will need to clone the repository first:\n```\n$ git clone https://github.com/chaoss/grimoirelab-perceval-weblate\n$ cd grimoirelab-perceval-weblate\n```\n\nThen use pip or Poetry to install the package along with its dependencies.\n\n#### Pip\nTo install the package from local directory run the following command:\n```\n$ pip install .\n```\nIn case you are a developer, you should install perceval-weblate in editable mode:\n```\n$ pip install -e .\n```\n\n#### Poetry\nWe use [poetry](https://python-poetry.org/) for dependency management and \npackaging. You can install it following its [documentation](https://python-poetry.org/docs/#installation).\nOnce you have installed it, you can install perceval-weblate and the dependencies in \na project isolated environment using:\n```\n$ poetry install\n```\nTo spaw a new shell within the virtual environment use:\n```\n$ poetry shell\n```\n\n## Examples\n\n### Weblate\n\n```\n$ perceval weblate\n```\n\n## License\n\nLicensed under GNU General Public License (GPL), version 3 or later.\n',
    'author': 'GrimoireLab Developers',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://chaoss.github.io/grimoirelab/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
