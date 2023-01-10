# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['helium_api_wrapper']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1',
 'haversine>=2.7.0,<3.0.0',
 'pandas>=1.5.1,<2.0.0',
 'pyarrow>=10.0.0,<11.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'sphinx-rtd-theme>=1.1.1,<2.0.0',
 'types-click>=7.1.8,<8.0.0',
 'types-requests>=2.28.11.5,<3.0.0.0']

entry_points = \
{'console_scripts': ['get-challenges = '
                     'helium_api_wrapper.__main__:get_challenges',
                     'get-device = helium_api_wrapper.__main__:get_device',
                     'get-hotspot = helium_api_wrapper.__main__:get_hotspot',
                     'get-hotspots = helium_api_wrapper.__main__:get_hotspots']}

setup_kwargs = {
    'name': 'helium-api-wrapper',
    'version': '0.0.1.dev1673382829',
    'description': 'Helium Api Wrapper',
    'long_description': "# Helium Api Wrapper\n\n[![PyPI](https://img.shields.io/pypi/v/helium-api-wrapper.svg)][pypi_]\n[![Status](https://img.shields.io/pypi/status/helium-api-wrapper.svg)][status]\n[![Python Version](https://img.shields.io/pypi/pyversions/helium-api-wrapper)][python version]\n[![License](https://img.shields.io/pypi/l/helium-api-wrapper)][license]\n\n[![Read the documentation at https://helium-api-wrapper.readthedocs.io/](https://img.shields.io/readthedocs/helium-api-wrapper/latest.svg?label=Read%20the%20Docs)][read the docs]\n[![Tests](https://github.com/emergotechnologies/helium-api-wrapper/workflows/Tests/badge.svg)][tests]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi_]: https://pypi.org/project/helium-api-wrapper/\n[status]: https://pypi.org/project/helium-api-wrapper/\n[python version]: https://pypi.org/project/helium-api-wrapper\n[read the docs]: https://helium-api-wrapper.readthedocs.io/\n[tests]: https://github.com/emergotechnologies/helium-api-wrapper/actions?workflow=Tests\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\n## Features\n\n- Load data from the Helium Blockchain API\n  - Get hotspots by address\n  - Get hotspots by location\n  - Get a list of hotspots\n  - Get challenges of a hotspot\n  - Get a list of challenges\n- Load Data from the Helium Console API\n  - Get device information by uuid\n\n## Requirements\n\n- Python 3.8+\n- [Poetry](https://python-poetry.org/)\n\n## Installation\n\nYou can install _Helium Api Wrapper_ via [pip] from [PyPI]:\n\n```console\n$ pip install helium-api-wrapper\n```\n\n## Usage\n\nYou can run the wrapper as a python module:\n\n```\npython -m helium_api_wrapper --help\npython -m helium_api_wrapper get-hotspots\npython -m helium_api_wrapper get-hotspot --address your-hotspot-address\n```\n\nTo personalise the settings command the file (using -, -- or CAPS to specify your settings) in a preferred terminal.\nTo list all possible settings run the --help command.\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [MIT license][license],\n_Helium Api Wrapper_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n## Credits\n\nThis project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/emergotechnologies/helium-api-wrapper/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/emergotechnologies/helium-api-wrapper/blob/main/LICENSE\n[contributor guide]: https://github.com/emergotechnologies/helium-api-wrapper/blob/main/CONTRIBUTING.md\n[command-line reference]: https://helium-api-wrapper.readthedocs.io/en/latest/usage.html\n",
    'author': 'Lukas Huber',
    'author_email': 'lukas.huber@fh-kufstein.ac.at',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/emergotechnologies/helium-api-wrapper',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
