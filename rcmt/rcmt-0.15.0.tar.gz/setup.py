# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rcmt',
 'rcmt.database',
 'rcmt.database.migrations',
 'rcmt.database.migrations.versions',
 'rcmt.source']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.18,<4.0.0',
 'PyGithub>=1.55,<2.0',
 'PyYAML>=5.4.1,<7.0.0',
 'alembic>=1.8.1,<2.0.0',
 'click>=8.0.1,<9.0.0',
 'colorama>=0.4.4,<0.5.0',
 'humanize>=4.2.3,<5.0.0',
 'mergedeep>=1.3.4,<2.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'python-gitlab>=2.10,<4.0',
 'python-slugify>=7.0.0,<8.0.0',
 'sqlalchemy[mypy]>=1.4.44,<2.0.0',
 'structlog>=21.1,<23.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['rcmt = rcmt.cli:main']}

setup_kwargs = {
    'name': 'rcmt',
    'version': '0.15.0',
    'description': '',
    'long_description': '# rcmt\n\nWith rcmt you can\n\n- create, modify or delete files across many repositories.\n- merge global settings with user-configured settings in repositories.\n- write your own tooling to manipulate files in repositories.\n\nTake a look at the [documentation](https://rcmt.readthedocs.io/) to learn more.\n\n## Development\n\n### Set up virtualenv and install dependencies\n\nRequirements:\n- [poetry](https://python-poetry.org/)\n\n```shell\npoetry install\n```\n\n### Run linters\n\nRequirements:\n- [Set up virtualenv and install dependencies](#set-up-virtualenv-and-install-dependencies) (only once)\n\n```shell\nmake lint\n```\n\n### Run tests\n\nRequirements:\n- [Set up virtualenv and install dependencies](#set-up-virtualenv-and-install-dependencies) (only once)\n\n```shell\nmake test\n```\n\n### Generate and view docs\n\nRequirements:\n- [Set up virtualenv and install dependencies](#set-up-virtualenv-and-install-dependencies) (only once)\n\n```shell\nmake docs\nopen ./docs/_build/html/index.html\n```\n\n### Create a new database migration\n\nRequirements:\n- [Set up virtualenv and install dependencies](#set-up-virtualenv-and-install-dependencies) (only once)\n\n1. Ensure that the database is on the latest revision:\n   ```shell\n   poetry run alembic -c ./hack/alembic.ini upgrade head\n   ```\n2. Add, change or delete a model in [rcmt/database/\\_\\_init\\_\\_.py](./rcmt/database/__init__.py).\n3. Let Alembic generate the new migration:\n   ```shell\n   poetry run alembic -c ./hack/alembic.ini revision --autogenerate -m \'Add model "Extension"\'\n   ```\n   **Note:** Alembic cannot detect every change. Review the newly generated file in [rcmt/database/migrations/versions](./rcmt/database/migrations/versions).\n   See [What does Autogenerate Detect (and what does it not detect?)](https://alembic.sqlalchemy.org/en/latest/autogenerate.html#what-does-autogenerate-detect-and-what-does-it-not-detect)\n   section in the documentation of Alembic for more details.\n',
    'author': 'Markus Meyer',
    'author_email': 'hydrantanderwand@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/wndhydrnt/rcmt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
