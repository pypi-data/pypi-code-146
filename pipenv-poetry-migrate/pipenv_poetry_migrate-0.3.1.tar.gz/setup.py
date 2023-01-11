# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pipenv_poetry_migrate']

package_data = \
{'': ['*']}

install_requires = \
['tomlkit>=0.5.11,<1.0.0', 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['pipenv-poetry-migrate = pipenv_poetry_migrate.cli:app']}

setup_kwargs = {
    'name': 'pipenv-poetry-migrate',
    'version': '0.3.1',
    'description': 'simple migration script, migrate pipenv to poetry',
    'long_description': '<h1 align="center">pipenv-poetry-migrate</h1>\n<p align="center">This is simple migration script, migrate pipenv to poetry.</p>\n\n<p align="center">\n    <a href="https://pypi.org/project/pipenv-poetry-migrate/"><img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/pipenv-poetry-migrate"></a>\n    <a href="https://pypi.org/project/pipenv-poetry-migrate/"><img src="https://img.shields.io/pypi/dm/pipenv-poetry-migrate" alt="PyPI - Downloads"></a>\n    <a href="https://github.com/yhino/pipenv-poetry-migrate/actions?query=workflow%3Abuild"><img src="https://github.com/yhino/pipenv-poetry-migrate/workflows/build/badge.svg" alt="build"></a>\n    <a href="https://codecov.io/gh/yhino/pipenv-poetry-migrate"><img src="https://codecov.io/gh/yhino/pipenv-poetry-migrate/branch/main/graph/badge.svg?token=LHZGQ8MMWT" alt="Codecov"></a>\n    <a href="https://app.fossa.com/projects/git%2Bgithub.com%2Fyhino%2Fpipenv-poetry-migrate?ref=badge_shield"><img src="https://app.fossa.com/api/projects/git%2Bgithub.com%2Fyhino%2Fpipenv-poetry-migrate.svg?type=shield" alt="FOSSA Status"></a>\n</p>\n\n## :rocket: Get Started\n\n### Installation\n\n    $ pip install -U poetry pipenv-poetry-migrate\n\n### Migration\n\n#### Step 1: Create `pyproject.toml` file\n\n    $ poetry init\n\n#### Step 2: Migrate\n\nTo migrate `Pipfile` to `pyproject.toml`.\n\n    $ pipenv-poetry-migrate -f Pipfile -t pyproject.toml\n\nWhen want to run dry-run mode:\n\n    $ pipenv-poetry-migrate -f Pipfile -t pyproject.toml -n\n\nDry-run mode is `pyproject.toml` file does not overwrite, results are displayed on standard output.\n\n> **Note**: \n> The default behavior is to migrate with the [group notation](https://python-poetry.org/docs/master/managing-dependencies/#dependency-groups), which has been available since Poetry 1.2.0.\n> If you want to migrate with `dev-dependencies` notation, please use the `--on-use-group-notation` option.\n> \n>     $ pipenv-poetry-migrate -f Pipfile -t pyproject.toml --no-use-group-notation\n\n#### Step 3: Generate lock file\n\n    $ poetry lock\n\nIf there is already a `poetry.lock` file, remove it first.\n\n#### Step 4: Installing dependencies\n\nTo install the defined dependencies for your project.\n\n    $ poetry install\n\n### Example output\n\nThis is an example of a Pipfile to be migrated.\n\n```toml\n[[source]]\nurl = "https://pypi.python.org/simple"\nverify_ssl = true\nname = "pypi"\n\n[packages]\nrequests = "*"\n\n[dev-packages]\npytest = "^5.2"\n```\n\nMigrate the above file to the following pyproject.toml.\n\n```toml\n[tool.poetry]\nname = "migration-sample"\nversion = "0.1.0"\ndescription = ""\nauthors = ["Yoshiyuki HINO <yhinoz@gmail.com>"]\n\n[tool.poetry.dependencies]\npython = "^3.7"\n\n[tool.poetry.group.dev.dependencies]\n\n[build-system]\nrequires = ["poetry-core"]\nbuild-backend = "poetry.core.masonry.api"\n```\n\nBy executing this script, pyproject.toml is rewritten as follows.\n\n```toml\n[tool.poetry]\nname = "migration-sample"\nversion = "0.1.0"\ndescription = ""\nauthors = ["Yoshiyuki HINO <yhinoz@gmail.com>"]\n\n[tool.poetry.dependencies]\npython = "^3.7"\nrequests = "*"\n\n[tool.poetry.group.dev.dependencies]\npytest = "^5.2"\n\n[build-system]\nrequires = ["poetry-core"]\nbuild-backend = "poetry.core.masonry.api"\n```\n\n## :handshake: Contributing\n\nTo run tests:\n\n1) `poetry install`  # get environment setup\n2) `make test`      # run the tests\n\nTest cases are in `tests/toml`, update `Pipfile` with additional entries and `expect_pyproject.toml` with expected output\n\n## :pencil: License\n\n[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fyhino%2Fpipenv-poetry-migrate.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fyhino%2Fpipenv-poetry-migrate?ref=badge_large)\n',
    'author': 'Yoshiyuki HINO',
    'author_email': 'yhinoz@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/yhino/pipenv-poetry-migrate',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
