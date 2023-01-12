# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['macrometa_source_oracle', 'macrometa_source_oracle.sync_strategies']

package_data = \
{'': ['*']}

install_requires = \
['c8connector==0.0.11',
 'cx-oracle>=8.3.0,<9.0.0',
 'pipelinewise-singer-python==1.2.0',
 'strict-rfc3339>=0.7,<0.8']

entry_points = \
{'console_scripts': ['macrometa-source-oracle = macrometa_source_oracle:main']}

setup_kwargs = {
    'name': 'macrometa-source-oracle',
    'version': '0.0.9',
    'description': 'Pipelinewise tap for reading from oracle databases. This includes support for PDBs.',
    'long_description': '# macrometa-source-oracle\n\n[![License: MIT](https://img.shields.io/badge/License-GPLv3-yellow.svg)](https://opensource.org/licenses/GPL-3.0)\n\n[Singer](https://www.singer.io/) tap that extracts data from a [Oracle](https://www.oracle.com/database/) database and produces JSON-formatted data following the [Singer spec](https://github.com/singer-io/getting-started/blob/master/docs/SPEC.md).\n\n## How to use it\n\n### Install and Run\n\nFirst, make sure Python 3 is installed on your system or follow these\ninstallation instructions for [Mac](http://docs.python-guide.org/en/latest/starting/install3/osx/) or\n[Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-ubuntu-16-04).\n\n\nIt\'s recommended to use a virtualenv:\n\n```bash\n  python3 -m venv venv\n  pip install macrometa-source-oracle\n```\n\nor from source using,\n1. Install poetry using https://python-poetry.org/docs/#installation\n2. Run \n    ```bash\n    poetry build\n    pip install dist/macrometa_source_oracle-<version>*.whl\n    ```\n\n### Configuration\n\nRunning the the tap requires a `config.json` file. \n\nExample configuration:\n\n```json\n{\n  "host": "dev.oracledb.io",\n  "port": 1521,\n  "user": "C##HELLO",\n  "password": "password",\n  "service_name": "ORCLCDB",\n  "filter_schemas": "C##HELLO",\n  "default_replication_method": "LOG_BASED",\n  "pdb_name": "ORCLPDB1",\n  "multitenant": true,\n  "scn_window_size": 10\n}\n```\n\nYou can run a discover run using the previous `config.json` file to acquire all the tables definition\n \n```\nmacrometa-source-oracle --config /tmp/config.json --discover >> /tmp/catalog.json\n```\n\nThen use the catalog.json to run a full export:\n\n```\nmacrometa-source-oracle --config /tmp/config.json --catalog /tmp/catalog.json\n```\n\n',
    'author': 'Macrometa',
    'author_email': 'info@macrometa.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://www.macrometa.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
