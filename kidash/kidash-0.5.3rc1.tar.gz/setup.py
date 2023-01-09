# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kidash', 'kidash.bin', 'tests']

package_data = \
{'': ['*'], 'tests': ['data/*']}

install_requires = \
['python-dateutil>=2.8.2,<3.0.0',
 'requests>=2.7.0,<3.0.0',
 'urllib3>=1.26,<2.0']

entry_points = \
{'console_scripts': ['kidash = kidash.bin.kidash:main']}

setup_kwargs = {
    'name': 'kidash',
    'version': '0.5.3rc1',
    'description': 'GrimoireLab script to manage Kibana dashboards from the command line',
    'long_description': '# Kidash [![Build Status](https://github.com/chaoss/grimoirelab-kidash/workflows/tests/badge.svg)](https://github.com/chaoss/grimoirelab-kidash/actions?query=workflow:tests+branch:master+event:push) [![Coverage Status](https://img.shields.io/coveralls/chaoss/grimoirelab-kidash.svg)](https://coveralls.io/r/chaoss/grimoirelab-kidash?branch=master) [![PyPI version](https://badge.fury.io/py/kidash.svg)](https://badge.fury.io/py/kidash)\n\nKidash is a tool for managing Kibana-related dashboards from the command line. The standard GrimoireLab dashboards\nare available in the [Sigils](https://github.com/chaoss/grimoirelab-sigils) repository.\n\n## Requirements\n\n * Python >= 3.7\n\nYou will also need some other libraries for running the tool, you can find the\nwhole list of dependencies in [pyproject.toml](pyproject.toml) file.\n\n## Installation\n\nThere are several ways to install Kidash on your system: packages or source \ncode using Poetry or pip.\n\n### PyPI:\n\nKidash can be installed using pip, a tool for installing Python packages. \nTo do it, run the next command:\n```\n$ pip install kidash\n```\n\n### Source code\n\nTo install from the source code you will need to clone the repository first:\n```\n$ git clone https://github.com/chaoss/grimoirelab-kidash\n$ cd grimoirelab-kidash\n```\n\nThen use pip or Poetry to install the package along with its dependencies.\n\n#### Pip\nTo install the package from local directory run the following command:\n```\n$ pip install .\n```\nIn case you are a developer, you should install kidash in editable mode:\n```\n$ pip install -e .\n```\n\n#### Poetry\nWe use [poetry](https://python-poetry.org/) for dependency management and \npackaging. You can install it following its [documentation](https://python-poetry.org/docs/#installation).\nOnce you have installed it, you can install kidash and the dependencies:\n```\n$ poetry install\n```\nTo spaw a new shell within the virtual environment use:\n```\n$ poetry shell\n```\n\n## Usage\n\n- Get a list of all options with:\n```\n$ kidash --help\n```\n\n- Import a dashboard:\n```buildoutcfg\nkidash -g -e <elasticsearch-url>:<port> --import <local-file-path>\nexample: kidash -g -e https://admin:admin@localhost:9200 --import ./overview.json\n```\n\n- Export a dashboard:\n```buildoutcfg\nkidash -g -e <elasticsearch-url> --dashboard <dashboard-id>* --export <local-file-path> --split-index-pattern\nexample: kidash -g -e https://admin:admin@localhost:9200 --dashboard overview --export overview.json\n```\n\n## License\n\nLicensed under GNU General Public License (GPL), version 3 or later.\n',
    'author': 'GrimoireLab Developers',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://chaoss.github.io/grimoirelab/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
