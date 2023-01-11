# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aw_core', 'aw_datastore', 'aw_datastore.storages', 'aw_query', 'aw_transform']

package_data = \
{'': ['*'], 'aw_core': ['schemas/*']}

install_requires = \
['TakeTheTime>=0.3.1,<0.4.0',
 'appdirs>=1.4.4,<2.0.0',
 'deprecation',
 'iso8601>=1.0.2,<2.0.0',
 'jsonschema>=4.3,<5.0',
 'peewee>=3.0.0,<4.0.0',
 'rfc3339-validator>=0.1.4,<0.2.0',
 'strict-rfc3339>=0.7,<0.8',
 'timeslot',
 'tomlkit']

extras_require = \
{'mongo': ['pymongo>=3.10.0,<4.0.0']}

entry_points = \
{'console_scripts': ['aw-cli = aw_cli.__main__:main']}

setup_kwargs = {
    'name': 'aw-core',
    'version': '0.5.11',
    'description': 'Core library for ActivityWatch',
    'long_description': 'aw-core\n=======\n\n[![GitHub Actions badge](https://github.com/ActivityWatch/aw-core/workflows/Build/badge.svg)](https://github.com/ActivityWatch/aw-core/actions)\n[![Code coverage](https://codecov.io/gh/ActivityWatch/aw-core/branch/master/graph/badge.svg)](https://codecov.io/gh/ActivityWatch/aw-core)\n[![PyPI](https://img.shields.io/pypi/v/aw-core)](https://pypi.org/project/aw-core/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Typechecking: Mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)\n\n\nCore library for ActivityWatch.\n\n\n## Modules\n\n - `aw_core`, contains basic datatypes and utilities, such as the `Event` class, helpers for configuration and logging, as well as schemas for buckets, events, and exports.\n - `aw_datastore`, contains the datastore classes used by aw-server-python.\n - `aw_transform`, all event-transforms used in queries.\n - `aw_query`, the query-language used by ActivityWatch.\n\n## Logging\n\nRun python with `LOG_LEVEL=debug` to use change the log level across all AW components\n\n## How to install\n\nTo install the latest git version directly from github without cloning, run\n`pip install git+https://github.com/ActivityWatch/aw-core.git`\n\nTo install from a cloned version, cd into the directory and run\n`poetry install` to install inside an virtualenv. If you want to install it\nsystem-wide it can be installed with `pip install .`, but that has the issue\nthat it might not get the exact version of the dependencies due to not reading\nthe poetry.lock file.\n\n',
    'author': 'Erik Bjäreholt',
    'author_email': 'erik@bjareho.lt',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://activitywatch.net/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
