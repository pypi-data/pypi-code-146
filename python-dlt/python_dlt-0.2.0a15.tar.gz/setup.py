# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dlt',
 'dlt.cli',
 'dlt.common',
 'dlt.common.configuration',
 'dlt.common.configuration.providers',
 'dlt.common.configuration.specs',
 'dlt.common.data_writers',
 'dlt.common.normalizers',
 'dlt.common.normalizers.json',
 'dlt.common.normalizers.names',
 'dlt.common.reflection',
 'dlt.common.runners',
 'dlt.common.schema',
 'dlt.common.storages',
 'dlt.dbt_runner',
 'dlt.destinations',
 'dlt.destinations.bigquery',
 'dlt.destinations.dummy',
 'dlt.destinations.postgres',
 'dlt.destinations.redshift',
 'dlt.extract',
 'dlt.helpers',
 'dlt.load',
 'dlt.normalize',
 'dlt.pipeline',
 'dlt.reflection']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'SQLAlchemy>=1.3.5,<2.0.0',
 'astunparse>=1.6.3,<2.0.0',
 'asyncstdlib>=3.10.5,<4.0.0',
 'cachetools>=5.2.0,<6.0.0',
 'click>=8.1.3,<9.0.0',
 'cron-descriptor>=1.2.32,<2.0.0',
 'gitpython>=3.1.29,<4.0.0',
 'hexbytes>=0.2.2,<0.3.0',
 'humanize>=4.4.0,<5.0.0',
 'json-logging==1.4.1rc0',
 'jsonlines>=2.0.0,<3.0.0',
 'makefun>=1.15.0,<2.0.0',
 'pathvalidate>=2.5.2,<3.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'pipdeptree>=2.3.3,<3.0.0',
 'prometheus-client>=0.11.0,<0.12.0',
 'pytz>=2022.6,<2023.0',
 'requests>=2.26.0,<3.0.0',
 'requirements-parser>=0.5.0,<0.6.0',
 'semver>=2.13.0,<3.0.0',
 'sentry-sdk>=1.4.3,<2.0.0',
 'setuptools>=65.6.0,<66.0.0',
 'simplejson>=3.17.5,<4.0.0',
 'tomlkit>=0.11.3,<0.12.0',
 'tqdm>=4.64.1,<5.0.0',
 'typing-extensions>=4.0.0,<5.0.0',
 'tzdata>=2022.1,<2023.0']

extras_require = \
{'bigquery': ['pyarrow>=8.0.0,<9.0.0'],
 'bigquery:python_version < "3.11"': ['grpcio>=1.50.0,<2.0.0',
                                      'google-cloud-bigquery>=2.26.0,<3.0.0',
                                      'google-cloud-bigquery-storage>=2.13.0,<3.0.0'],
 'dbt': ['dbt-core>=1.1.0,<1.2.0', 'dbt-redshift>=1.0.0,<1.2.0'],
 'dbt:python_version < "3.11"': ['dbt-bigquery>=1.0.0,<1.2.0'],
 'gcp': ['pyarrow>=8.0.0,<9.0.0'],
 'gcp:python_version < "3.11"': ['grpcio>=1.50.0,<2.0.0',
                                 'google-cloud-bigquery>=2.26.0,<3.0.0',
                                 'google-cloud-bigquery-storage>=2.13.0,<3.0.0'],
 'postgres': ['psycopg2-binary>=2.9.1,<3.0.0'],
 'postgres:platform_python_implementation == "PyPy"': ['psycopg2cffi>=2.9.0,<3.0.0'],
 'redshift': ['psycopg2-binary>=2.9.1,<3.0.0'],
 'redshift:platform_python_implementation == "PyPy"': ['psycopg2cffi>=2.9.0,<3.0.0']}

entry_points = \
{'console_scripts': ['dlt = dlt.cli._dlt:main']}

setup_kwargs = {
    'name': 'python-dlt',
    'version': '0.2.0a15',
    'description': 'DLT is an open-source python-native scalable data loading framework that does not require any devops efforts to run.',
    'long_description': '![](https://github.com/dlt-hub/dlt/raw/devel/docs/DLT-Pacman-Big.gif)\n\n<p align="center">\n\n[![PyPI version](https://badge.fury.io/py/python-dlt.svg)](https://pypi.org/project/python-dlt/)\n[![LINT Badge](https://github.com/scale-vector/dlt/actions/workflows/lint.yml/badge.svg)](https://github.com/scale-vector/dlt/actions/workflows/lint.yml)\n[![TEST COMMON Badge](https://github.com/scale-vector/dlt/actions/workflows/test_common.yml/badge.svg)](https://github.com/scale-vector/dlt/actions/workflows/test_common.yml)\n[![TEST REDSHIFT Badge](https://github.com/scale-vector/dlt/actions/workflows/test_loader_redshift.yml/badge.svg)](https://github.com/scale-vector/dlt/actions/workflows/test_loader_redshift.yml)\n[![TEST BIGQUERY Badge](https://github.com/scale-vector/dlt/actions/workflows/test_loader_bigquery.yml/badge.svg)](https://github.com/scale-vector/dlt/actions/workflows/test_loader_bigquery.yml)\n\n</p>\n\n# data load tool (dlt)\n\n**data load tool (dlt)** is a simple, open source Python library that makes data loading easy\n- Automatically turn the JSON returned by any API into a live dataset stored wherever you want it\n- `pip install python-dlt` and then include `import dlt` to use it in your Python loading script\n- The **dlt** library is licensed under the Apache License 2.0, so you can use it for free forever\n\nRead more about it on the [dlt Docs](https://dlthub.com/docs)\n\n# semantic versioning\n`python-dlt` will follow the semantic versioning with [`MAJOR.MINOR.PATCH`](https://peps.python.org/pep-0440/#semantic-versioning) pattern. Currently we do **pre-release versioning** with major version being 0.\n- `minor` version change means breaking changes\n- `patch` version change means new features that should be backward compatible\n- any suffix change ie. `a10` -> `a11` is a patch\n\n# development\n`python-dlt` uses `poetry` to manage, build and version the package. It also uses `make` to automate tasks. To start\n```sh\nmake install-poetry  # will install poetry, to be run outside virtualenv\n```\nthen\n```sh\nmake dev  # will install all deps including dev\n```\nExecuting `poetry shell` and working in it is very convenient at this moment.\n\n## python version\nUse python 3.8 for development which is the lowest supported version for `python-dlt`. You\'ll need `distutils` and `venv`:\n\n```shell\nsudo apt-get install python3.8\nsudo apt-get install python3.8-distutils\nsudo apt install python3.8-venv\n```\nYou may also use `pyenv` as [poetry](https://python-poetry.org/docs/managing-environments/) suggests.\n\n## bumping version\nPlease use `poetry version prerelease` to bump patch and then `make build-library` to apply changes. The source of the version is `pyproject.toml` and we use poetry to manage it.\n\n## testing and linting\n`python-dlt` uses `mypy` and `flake8` with several plugins for linting. We do not reorder imports or reformat code.\n\n`pytest` is used as test harness. `make test-common` will run tests of common components and does not require any external resources.\n\n### testing destinations\nTo test destinations use `make test`. You will need following external resources\n1. `BigQuery` project\n2. `Redshift` cluster\n3. `Postgres` instance. You can find a docker compose for postgres instance [here](tests/postgres/docker-compose.yml)\n\nSee `tests/.example.env` for the expected environment variables. Then create `tests/.env` from it. You configure the tests as you would configure the dlt pipeline.\nWe\'ll provide you with access to the resources above if you wish to test locally.\n\n## publishing\n\n1. Make sure that you are on `devel` branch and you have the newest code that passed all tests on CI.\n2. Verify the current version with `poetry version`\n3. You\'ll need `pypi` access token and use `poetry config pypi-token.pypi your-api-token` then\n```\nmake publish-library\n```\n4. Make a release on github, use version and git tag as release name\n\n## contributing\n\nTo contribute via pull request:\n1. Create an issue with your idea for a feature etc.\n2. Write your code and tests\n3. Lint your code with `make lint`. Test the common modules with `make test-common`\n4. If you work on a destination code then contact us to get access to test destinations\n5. Create a pull request\n',
    'author': 'dltHub Inc.',
    'author_email': 'services@dlthub.com',
    'maintainer': 'Marcin Rudolf',
    'maintainer_email': 'marcin@dlthub.com',
    'url': 'https://github.com/dlt-hub',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
