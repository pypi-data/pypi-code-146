# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ssb_project_cli',
 'ssb_project_cli.ssb_project',
 'ssb_project_cli.ssb_project.build',
 'ssb_project_cli.ssb_project.clean',
 'ssb_project_cli.ssb_project.create']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.27,<4.0.0',
 'PyGithub>=1.55,<2.0',
 'certifi>=2022.12.7,<2023.0.0',
 'click>=8.0.1',
 'cruft>=2.11.1,<3.0.0',
 'dparse>=0.6.2,<0.7.0',
 'psutil>=5.9.4,<6.0.0',
 'questionary>=1.10.0,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'rich>=12.5.1,<13.0.0',
 'typer>=0.6.1,<0.7.0',
 'types-toml>=0.10.8,<0.11.0',
 'urllib3>=1.26.12,<2.0.0']

entry_points = \
{'console_scripts': ['ssb-project = ssb_project_cli.__main__:main']}

setup_kwargs = {
    'name': 'ssb-project-cli',
    'version': '1.0.13',
    'description': 'SSB Project CLI',
    'long_description': '# SSB Project CLI\n\n[![PyPI](https://img.shields.io/pypi/v/ssb-project-cli.svg)][pypi status]\n[![Status](https://img.shields.io/pypi/status/ssb-project-cli.svg)][pypi status]\n[![Python Version](https://img.shields.io/pypi/pyversions/ssb-project-cli)][pypi status]\n[![License](https://img.shields.io/pypi/l/ssb-project-cli)][license]\n\n[![Read the documentation](https://img.shields.io/badge/docs-Github%20Pages-purple)](https://statisticsnorway.github.io/ssb-project-cli/)\n[![Tests](https://github.com/statisticsnorway/ssb-project-cli/workflows/Tests/badge.svg)][tests]\n[![Codecov](https://codecov.io/gh/statisticsnorway/ssb-project-cli/branch/main/graph/badge.svg)][codecov]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi status]: https://pypi.org/project/ssb-project-cli/\n[read the docs]: https://ssb-project-cli.readthedocs.io/\n[tests]: https://github.com/statisticsnorway/ssb-project-cli/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/statisticsnorway/ssb-project-cli\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\n## Features\n\n![Help text](docs/assets/cli_help_screenshot.png)\n\n- Create a new project quickly and easily with `ssb-project create`.\n- Your colleagues can quickly get started when you share the project with them with `ssb-project build`.\n- Includes:\n  - Local directory structure\n  - Virtual Environment\n  - Kernel for use on Jupyter\n  - Github repo (if desired)\n- The project will follow the most recent SSB guidelines for security and quality.\n- It will always be possible to update existing projects as guidelines change.\n\n## Installation\n\nYou can install _SSB Project CLI_ via [pip] from [PyPI]:\n\n```console\npip install ssb-project-cli\n```\n\n## Releasing a new version\n\nTo release a new version of the CLI, run the following sequence.\n\n```console\ngit switch --create release main\n```\n\n```console\npoetry version <version>\n```\n\n```console\ngit commit --message="<project> <version>" pyproject.toml\n```\n\n```console\ngit push origin release\n```\n\n## Contributing\n\n### Setup\n\n1. [Install dependencies](https://cookiecutter-hypermodern-python.readthedocs.io/en/latest/guide.html#installation)\n1. [Install pre-commit hooks](https://cookiecutter-hypermodern-python.readthedocs.io/en/latest/guide.html#running-pre-commit-from-git)\n1. Run tests: `nox -r` ([More information here](https://cookiecutter-hypermodern-python.readthedocs.io/en/latest/guide.html#using-nox))\n1. Run the help command: `poetry run ssb-project --help`\n\n## License\n\nDistributed under the terms of the [MIT license][license],\n_SSB Project CLI_ is free and open source software.\n\n<!-- github-only -->\n\n[license]: https://github.com/statisticsnorway/ssb-project-cli/blob/main/LICENSE\n',
    'author': 'Statistics Norway',
    'author_email': 'stat-dev@ssb.no',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/statisticsnorway/ssb-project-cli',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
