# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sqlalchemy_uow']

package_data = \
{'': ['*']}

install_requires = \
['hydra-core>=1.1.1,<2.0.0']

setup_kwargs = {
    'name': 'sqlalchemy-uow',
    'version': '0.0.6',
    'description': 'Unit of Work for SQLAlchemy project',
    'long_description': "# sqlalchemy-uow\n\nUnit of Work for SQLAlchemy project\n\n______________________________________________________________________\n[![PyPI Status](https://badge.fury.io/py/sqlalchemy_uow.svg)](https://pypi.org/project/sqlalchemy_uow/)\n[![Documentation](https://img.shields.io/badge/docs-passing-green)](https://barbara73.github.io/sqlalchemy_uow/sqlalchemy_uow.html)\n[![License](https://img.shields.io/github/license/barbara73/sqlalchemy_uow)](https://github.com/barbara73/sqlalchemy_uow/blob/main/LICENSE)\n[![LastCommit](https://img.shields.io/github/last-commit/barbara73/sqlalchemy_uow)](https://github.com/barbara73/sqlalchemy_uow/commits/main)\n[![Code Coverage](https://img.shields.io/badge/Coverage-0%25-red.svg)](https://github.com/barbara73/sqlalchemy_uow/tree/main/tests)\n[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.0-4baaaa.svg)](https://github.com/barbara73/sqlalchemy_uow/blob/main/CODE_OF_CONDUCT.md)\n\n\nDevelopers:\n\n- Barbara Jesacher (barbarajesacher@icloud.com)\n\n\n## Setup\n\n### Set up the environment\n\n1. Run `make install`, which installs Poetry (if it isn't already installed), sets up a virtual environment and all Python dependencies therein.\n2. Run `source .venv/bin/activate` to activate the virtual environment.\n\n### Install new packages\n\nTo install new PyPI packages, run:\n\n```\n$ poetry add <package-name>\n```\n\n### Auto-generate API documentation\n\nTo auto-generate API document for your project, run:\n\n```\n$ make docs\n```\n\nTo view the documentation, run:\n\n```\n$ make view-docs\n```\n\n## Tools used in this project\n* [Poetry](https://towardsdatascience.com/how-to-effortlessly-publish-your-python-package-to-pypi-using-poetry-44b305362f9f): Dependency management\n* [hydra](https://hydra.cc/): Manage configuration files\n* [pre-commit plugins](https://pre-commit.com/): Automate code reviewing formatting\n* [pdoc](https://github.com/pdoc3/pdoc): Automatically create an API documentation for your project\n\n## Project structure\n```\n.\n├── .flake8\n├── .github\n│\xa0\xa0 └── workflows\n│\xa0\xa0     ├── ci.yaml\n│\xa0\xa0     └── docs.yaml\n├── .gitignore\n├── .pre-commit-config.yaml\n├── CHANGELOG.md\n├── CODE_OF_CONDUCT.md\n├── CONTRIBUTING.md\n├── LICENSE\n├── README.md\n├── config\n│\xa0\xa0 ├── __init__.py\n│\xa0\xa0 └── config.yaml\n├── data\n├── makefile\n├── models\n├── notebooks\n├── poetry.toml\n├── pyproject.toml\n├── src\n│\xa0\xa0 ├── scripts\n│\xa0\xa0 │\xa0\xa0 ├── fix_dot_env_file.py\n│\xa0\xa0 │\xa0\xa0 └── versioning.py\n│\xa0\xa0 └── sqlalchemy_uow\n│\xa0\xa0     └── __init__.py\n└── tests\n    └── __init__.py\n```\n",
    'author': 'Barbara Jesacher',
    'author_email': 'barbarajesacher@icloud.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
