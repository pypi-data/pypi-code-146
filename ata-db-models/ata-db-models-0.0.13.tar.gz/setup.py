# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ata_db_models']

package_data = \
{'': ['*']}

install_requires = \
['boto3-stubs[ssm]==1.26.13',
 'boto3==1.26.13',
 'psycopg2==2.9.5',
 'sqlmodel==0.0.8']

setup_kwargs = {
    'name': 'ata-db-models',
    'version': '0.0.13',
    'description': 'Database models and migrations for Automating the Ask.',
    'long_description': '# ata-db-models\n\n<!-- [![Release](https://img.shields.io/github/v/release/LocalAtBrown/ata-db-models)](https://img.shields.io/github/v/release/LocalAtBrown/ata-db-models) -->\n<!-- [![Build status](https://img.shields.io/github/workflow/status/LocalAtBrown/ata-db-models/merge-to-main)](https://img.shields.io/github/workflow/status/LocalAtBrown/ata-db-models/merge-to-main) -->\n\n[![Python version](https://img.shields.io/badge/python_version-3.9-blue)](https://github.com/psf/black)\n[![Code style with black](https://img.shields.io/badge/code_style-black-000000.svg)](https://github.com/psf/black)\n[![More style with flake8](https://img.shields.io/badge/code_style-flake8-blue)](https://flake8.pycqa.org)\n[![Imports with isort](https://img.shields.io/badge/%20imports-isort-blue)](https://pycqa.github.io/isort/)\n[![Type checking with mypy](https://img.shields.io/badge/type_checker-mypy-blue)](https://mypy.readthedocs.io)\n[![License](https://img.shields.io/github/license/LocalAtBrown/ata-db-models)](https://img.shields.io/github/license/LocalAtBrown/ata-db-models)\n\nDatabase models and migrations for Automating the Ask.\n\n## Usage\n\n### As a package\n\nWe use [SQLModel](https://sqlmodel.tiangolo.com/), a layer on top of SQLAlchemy with Pydantic, to define our tables.\nThis is useful because we can import this package to interact with the tables AND have Pydantic objects in Python\nthat correspond to a row in the table.\n\nTo install the package from PyPi, run: `pip install ata-db-models`. Check existing versions \n[here](https://pypi.org/project/ata-db-models/).\n\n### Initialize a new cluster\n\nIf you want to initialize a fresh database cluster, pass in the env vars to connect to the cluster and run `init_db`.\nIf the target cluster has IP restrictions, make sure your IP address is a valid access point.\n\nAn example run with fake credentials (from the root dir of this project with the virtual env\nactivated):\n`HOST=fakehost USER=fakeuser PASSWORD=fakepw DB_NAME=postgres python src/init_db.py`\n\nNo `PORT` is passed because the default port is 5432, the standard for Postgres.\n\n### Migrations\n\nSo you made some changes to what tables there are, what columns there are, indices, etc. and you\'d like to\nupdate the databases. This is what alembic is for!\n\nTo generate a new revision after you\'ve updated the models:\n\n1. Run this from the root of the project: `DB_CONNECTION_STRING=\'postgresql://user:password@host:port/db_name\' alembic revision --autogenerate -m "message"`\n2. Check the `/alembic/versions/` directory for the new revision and verify that it does what you want it to\n3. Run this from the root of the project: `DB_CONNECTION_STRING=\'postgresql://user:password@host:port/db_name\' alembic upgrade head`\n\n\n## Development\n\nThis project uses [Poetry](https://python-poetry.org/) to manage dependencies. It also helps with pinning dependency and python\nversions. We also use [pre-commit](https://pre-commit.com/) with hooks for [isort](https://pycqa.github.io/isort/),\n[black](https://github.com/psf/black), and [flake8](https://flake8.pycqa.org/en/latest/) for consistent code style and\nreadability. Note that this means code that doesn\'t meet the rules will fail to commit until it is fixed.\n\nWe use [mypy](https://mypy.readthedocs.io/en/stable/index.html) for static type checking. This can be run [manually](#run-static-type-checking),\nand the CI runs it on PRs to the `main` branch. We also use [pytest](https://docs.pytest.org/en/7.2.x/) to run our tests.\nThis can be run [manually](#run-tests) and the CI runs it on PRs to the `main` branch.\n\n### Setup\n\n1. [Install Poetry](https://python-poetry.org/docs/#installation).\n2. Run `poetry install --no-root`\n3. Run `source $(poetry env list --full-path)/bin/activate && pre-commit install && deactivate` to set up `pre-commit`\n\nYou\'re all set up! Your local environment should include all dependencies, including dev dependencies like `black`.\nThis is done with Poetry via the `poetry.lock` file.\n\n### Run Code Format and Linting\n\nTo manually run isort, black, and flake8 all in one go, simply run `pre-commit run --all-files`. Explore the `pre-commit` docs (linked above)\nto see more options.\n\n### Run Static Type Checking\n\nTo manually run mypy, simply run `mypy` from the root directory of the project. It will use the default configuration\nspecified in `pyproject.toml`.\n\n### Update Dependencies\n\nTo update dependencies in your local environment, make changes to the `pyproject.toml` file then run `poetry update` from the root directory of the project.\n\n### Run Tests\n\nTo manually run rests, you need to have a Postgres instance running locally on port 5432. One way to do this\nis to run a Docker container, then run the tests while it is active.\n\n1. (If you don\'t already have the image locally) Run `docker pull postgres`\n2. Run `docker run --rm --name postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_HOST_AUTH_METHOD=trust -p 127.0.0.1:5432:5432/tcp postgres`\n3. Run `DB_NAME=postgres pytest tests` from the root directory of the project. Explore the `pytest` docs (linked above)\nto see more options.\n\nNote that if you decide to run the Postgres container with different credentials (a different password, port, etc.) or\nvia a different method, you will likely need to update the test file to point to the correct Postgres instance.\n\nAdditionally, if you want to re-run the tests, you want to make sure you start over from a fresh Postgres\ninstance. If you run Postgres via Docker, you can simply `ctrl-C` to stop the image and start a new one.\n',
    'author': 'Raaid Arshad',
    'author_email': 'raaid@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/LocalAtBrown/ata-models',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
