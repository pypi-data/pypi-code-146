# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pontos',
 'pontos.changelog',
 'pontos.git',
 'pontos.github',
 'pontos.github.actions',
 'pontos.github.api',
 'pontos.github.models',
 'pontos.github.script',
 'pontos.models',
 'pontos.nvd',
 'pontos.nvd.cpe',
 'pontos.nvd.cve',
 'pontos.nvd.models',
 'pontos.release',
 'pontos.terminal',
 'pontos.testing',
 'pontos.updateheader',
 'pontos.updateheader.templates.AGPL-3.0-or-later',
 'pontos.updateheader.templates.GPL-2.0-or-later',
 'pontos.updateheader.templates.GPL-3.0-or-later',
 'pontos.version',
 'scripts',
 'scripts.github',
 'tests',
 'tests.changelog',
 'tests.git',
 'tests.github',
 'tests.github.actions',
 'tests.github.api',
 'tests.github.models',
 'tests.github.script',
 'tests.models',
 'tests.nvd',
 'tests.nvd.cpe',
 'tests.nvd.cve',
 'tests.nvd.models',
 'tests.release',
 'tests.terminal',
 'tests.testing',
 'tests.updateheader',
 'tests.version']

package_data = \
{'': ['*'], 'pontos.updateheader': ['templates/GPL-2.0-only/*']}

modules = \
['poetry']
install_requires = \
['colorful>=0.5.4,<0.6.0',
 'httpx[http2]>=0.23.0,<0.24.0',
 'packaging>=20.3',
 'python-dateutil>=2.8.2,<3.0.0',
 'rich>=12.4.4,<13.0.0',
 'tomlkit>=0.5.11']

extras_require = \
{':python_version < "3.8"': ['typing-extensions>=4.4.0,<5.0.0']}

entry_points = \
{'console_scripts': ['pontos = pontos:main',
                     'pontos-changelog = pontos.changelog:main',
                     'pontos-github = pontos.github:main',
                     'pontos-github-actions = pontos.github.actions:main',
                     'pontos-github-script = pontos.github.script:main',
                     'pontos-nvd-cpe = pontos.nvd.cpe:cpe_main',
                     'pontos-nvd-cpes = pontos.nvd.cpe:cpes_main',
                     'pontos-nvd-cve = pontos.nvd.cve:cve_main',
                     'pontos-nvd-cves = pontos.nvd.cve:cves_main',
                     'pontos-release = pontos.release:main',
                     'pontos-update-header = pontos.updateheader:main',
                     'pontos-version = pontos.version:main']}

setup_kwargs = {
    'name': 'pontos',
    'version': '23.1.0',
    'description': 'Common utilities and tools maintained by Greenbone Networks',
    'long_description': '![Greenbone Logo](https://www.greenbone.net/wp-content/uploads/gb_new-logo_horizontal_rgb_small.png)\n\n# Pontos - Greenbone Python Utilities and Tools <!-- omit in toc -->\n\n[![GitHub releases](https://img.shields.io/github/release/greenbone/pontos.svg)](https://github.com/greenbone/pontos/releases)\n[![PyPI release](https://img.shields.io/pypi/v/pontos.svg)](https://pypi.org/project/pontos/)\n[![code test coverage](https://codecov.io/gh/greenbone/pontos/branch/main/graph/badge.svg)](https://codecov.io/gh/greenbone/pontos)\n[![Build and test](https://github.com/greenbone/pontos/actions/workflows/ci-python.yml/badge.svg)](https://github.com/greenbone/pontos/actions/workflows/ci-python.yml)\n\nThe **pontos** Python package is a collection of utilities, tools, classes and\nfunctions maintained by [Greenbone Networks].\n\nPontos is the German name of the Greek titan [Pontus](https://en.wikipedia.org/wiki/Pontus_(mythology)),\nthe titan of the sea.\n\n## Table of Contents <!-- omit in toc -->\n\n- [Documentation](#documentation)\n- [Installation](#installation)\n  - [Requirements](#requirements)\n  - [Install using pip](#install-using-pip)\n  - [Install using poetry](#install-using-poetry)\n- [Development](#development)\n- [Maintainer](#maintainer)\n- [Contributing](#contributing)\n- [License](#license)\n\n## Documentation\n\nThe documentation for pontos can be found at https://greenbone.github.io/pontos/. Please refer to the documentation for more details as this README just gives a short overview.\n\n## Installation\n\n### Requirements\n\nPython 3.7 and later is supported.\n\n### Install using pip\n\npip 19.0 or later is required.\n\n> **Note**: All commands listed here use the general tool names. If some of\n> these tools are provided by your distribution, you may need to explicitly use\n> the Python 3 version of the tool, e.g. **`pip3`**.\n\nYou can install the latest stable release of **pontos** from the Python\nPackage Index (pypi) using [pip]\n\n    pip install --user pontos\n\n### Install using poetry\n\nBecause **pontos** is a Python library you most likely need a tool to\nhandle Python package dependencies and Python environments. Therefore we\nstrongly recommend using [pipenv] or [poetry].\n\nYou can install the latest stable release of **pontos** and add it as\na dependency for your current project using [poetry]\n\n    poetry add pontos\n\nFor installation via pipenv please take a look at their [documentation][pipenv].\n\n## Development\n\n**pontos** uses [poetry] for its own dependency management and build\nprocess.\n\nFirst install poetry via pip\n\n    pip install --user poetry\n\nAfterwards run\n\n    poetry install\n\nin the checkout directory of **pontos** (the directory containing the\n`pyproject.toml` file) to install all dependencies including the packages only\nrequired for development.\n\nAfterwards activate the git hooks for auto-formatting and linting via\n[autohooks].\n\n    poetry run autohooks activate\n\nValidate the activated git hooks by running\n\n    poetry run autohooks check\n\n## Maintainer\n\nThis project is maintained by [Greenbone Networks GmbH][Greenbone Networks]\n\n## Contributing\n\nYour contributions are highly appreciated. Please\n[create a pull request](https://github.com/greenbone/pontos/pulls)\non GitHub. Bigger changes need to be discussed with the development team via the\n[issues section at GitHub](https://github.com/greenbone/pontos/issues)\nfirst.\n\n## License\n\nCopyright (C) 2020-2022 [Greenbone Networks GmbH][Greenbone Networks]\n\nLicensed under the [GNU General Public License v3.0 or later](LICENSE).\n\n[Greenbone Networks]: https://www.greenbone.net/\n[poetry]: https://python-poetry.org/\n[pip]: https://pip.pypa.io/\n[pipenv]: https://pipenv.pypa.io/\n[autohooks]: https://github.com/greenbone/autohooks\n',
    'author': 'Greenbone Networks GmbH',
    'author_email': 'info@greenbone.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/greenbone/pontos/',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
