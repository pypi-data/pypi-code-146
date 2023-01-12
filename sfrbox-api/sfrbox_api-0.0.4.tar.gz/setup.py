# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sfrbox_api', 'sfrbox_api.cli']

package_data = \
{'': ['*']}

install_requires = \
['defusedxml>=0.7.1', 'httpx>=0.23.1', 'pydantic>=1.10.2']

extras_require = \
{'cli': ['click>=8.0.1']}

entry_points = \
{'console_scripts': ['sfrbox-api = sfrbox_api.__main__:main']}

setup_kwargs = {
    'name': 'sfrbox-api',
    'version': '0.0.4',
    'description': 'SFR Box API',
    'long_description': "# SFR Box API\n\n[![PyPI](https://img.shields.io/pypi/v/sfrbox-api.svg)][pypi_]\n[![Status](https://img.shields.io/pypi/status/sfrbox-api.svg)][status]\n[![Python Version](https://img.shields.io/pypi/pyversions/sfrbox-api)][python version]\n[![License](https://img.shields.io/pypi/l/sfrbox-api)][license]\n\n[![Read the documentation at https://sfrbox-api.readthedocs.io/](https://img.shields.io/readthedocs/sfrbox-api/latest.svg?label=Read%20the%20Docs)][read the docs]\n[![Tests](https://github.com/hacf-fr/sfrbox-api/workflows/Tests/badge.svg)][tests]\n[![Codecov](https://codecov.io/gh/hacf-fr/sfrbox-api/branch/main/graph/badge.svg)][codecov]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi_]: https://pypi.org/project/sfrbox-api/\n[status]: https://pypi.org/project/sfrbox-api/\n[python version]: https://pypi.org/project/sfrbox-api\n[read the docs]: https://sfrbox-api.readthedocs.io/\n[tests]: https://github.com/hacf-fr/sfrbox-api/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/hacf-fr/sfrbox-api\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\n## Features\n\n- TODO\n\n## Requirements\n\n- TODO\n\n## Installation\n\nYou can install _SFR Box API_ via [pip] from [PyPI]:\n\n```console\n$ pip install sfrbox-api\n```\n\n## Usage\n\nPlease see the [Command-line Reference] for details.\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [MIT license][license],\n_SFR Box API_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n## Credits\n\nThis project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/hacf-fr/sfrbox-api/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/hacf-fr/sfrbox-api/blob/main/LICENSE\n[contributor guide]: https://github.com/hacf-fr/sfrbox-api/blob/main/CONTRIBUTING.md\n[command-line reference]: https://sfrbox-api.readthedocs.io/en/latest/usage.html\n",
    'author': 'epenet',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/hacf-fr/sfrbox-api',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
