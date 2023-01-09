# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['loglicense']

package_data = \
{'': ['*']}

install_requires = \
['certifi>=2022.12.07,<2023.0.0',
 'gitpython>=3.1.30,<4.0.0',
 'pathlib>=1.0.1,<2.0.0',
 'tabulate>=0.8.10,<0.9.0',
 'toml>=0.10.2,<0.11.0',
 'typer>=0.6.1,<0.7.0',
 'types-tabulate>=0.8.11,<0.9.0',
 'types-toml>=0.10.8,<0.11.0']

entry_points = \
{'console_scripts': ['loglicense = loglicense.__main__:app']}

setup_kwargs = {
    'name': 'loglicense',
    'version': '0.1.7',
    'description': 'Log License',
    'long_description': "# Log License\n\n[![PyPI](https://img.shields.io/pypi/v/loglicense.svg)][pypi_]\n![Downloads](https://img.shields.io/pypi/dm/loglicense)\n[![Status](https://img.shields.io/pypi/status/loglicense.svg)][status]\n[![Python Version](https://img.shields.io/pypi/pyversions/loglicense)][python version]\n[![License](https://img.shields.io/pypi/l/loglicense)][license]\n\n[![Read the documentation at https://loglicense.readthedocs.io/](https://img.shields.io/readthedocs/loglicense/latest.svg?label=Read%20the%20Docs)][read the docs]\n[![Tests](https://github.com/martincjespersen/loglicense/workflows/Tests/badge.svg)][tests]\n[![Codecov](https://codecov.io/gh/martincjespersen/loglicense/branch/main/graph/badge.svg)][codecov]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi_]: https://pypi.org/project/loglicense/\n[status]: https://pypi.org/project/loglicense/\n[python version]: https://pypi.org/project/loglicense\n[read the docs]: https://loglicense.readthedocs.io/\n[tests]: https://github.com/martincjespersen/loglicense/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/martincjespersen/loglicense\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\nA tool for helping developers staying compliant within their software projects. The tool crawls dependencies and logs their licenses, allowing to document and restrict certain licenses within a software project.\n\n**DISCLAIMER**: _There is no guarentee that all sublicenses or licenses will be identified and reported. For highest ensurance, use lock files to also catch sub-dependencies. However, this only looks within the given package manager, meaning C libraries and alike will not be reported here._\n\n## Features\n\n- Report and save log of licenses included in project\n- Check coverage of packages supported accepted licenses\n- Supporting pre-commits with coverage thresholds and allowing manual validation of unknown license types\n\n### Supported dependency files\n\nThough the tool supports multiple file types, it is **highly recommended** to use lock files or do a ´pip freeze > requirements.txt´ in order to ensure all sub-dependencies are also evaluated for their license.\n\n- poetry.lock\n- pyproject.toml (traditional and poetry)\n- requirements.txt (--develop adds search for requirements_dev.txt)\n\n### Supported package managers\n\n- pypi\n\n## Installation\n\nYou can install _Log License_ via [pip] from [PyPI]:\n\n```console\n$ pip install loglicense\n```\n\nor using [Poetry]\n\n```console\n$ poetry add loglicense\n```\n\n## Quick example\n\nPlease see the [Command-line Reference] for details.\n\n```console\n$ loglicense report path_to/poetry.lock\n```\n\nExample output:\n\n```console\n| Name               | License                            |\n|:-------------------|:-----------------------------------|\n| click              | BSD-3-Clause                       |\n| colorama           | BSD                                |\n| importlib-metadata | Apache Software License            |\n| pathlib            | MIT License                        |\n| tabulate           | MIT                                |\n| toml               | MIT                                |\n| typer              | MIT License                        |\n| typing-extensions  | Python Software Foundation License |\n| zipp               | MIT License                        |\n```\n\nAlternatively you can let it search the executed directory for any supported file\n\n```console\n$ loglicense report\n```\n\n## Features to implement\n\n- Support npmjs package manager (and package.json/package-lock.json)\n- Support Pipfile, Pipfile.lock, conda.yaml, pip freeze\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [Apache 2.0 license][license],\n_Log License_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n## Credits\n\nThis project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/martincjespersen/loglicense/issues\n[pip]: https://pip.pypa.io/\n\nThis project is greatly inspired by [dep-license] created by [Abdulelah Bin Mahfoodh].\n\n[dep-license]: https://github.com/abduhbm/dep-license\n[abdulelah bin mahfoodh]: https://github.com/abduhbm\n[poetry]: https://python-poetry.org/\n\n<!-- github-only -->\n\n[license]: https://github.com/martincjespersen/loglicense/blob/main/LICENSE\n[contributor guide]: https://github.com/martincjespersen/loglicense/blob/main/CONTRIBUTING.md\n[command-line reference]: https://loglicense.readthedocs.io/en/latest/usage.html\n",
    'author': 'Martin Closter Jespersen',
    'author_email': 'martincjespersen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/martincjespersen/loglicense',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
