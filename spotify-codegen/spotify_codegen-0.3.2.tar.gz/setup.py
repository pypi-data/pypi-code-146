# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['spotifycodegen']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1',
 'colorthief>=0.2.1,<0.3.0',
 'pillow>=9.3.0,<10.0.0',
 'spotipy>=2.21.0,<3.0.0',
 'tqdm>=4.64.1,<5.0.0']

entry_points = \
{'console_scripts': ['spotifycodegen = spotifycodegen.cli:cli']}

setup_kwargs = {
    'name': 'spotify-codegen',
    'version': '0.3.2',
    'description': 'spotify-codegen',
    'long_description': '# spotify-codegen\n\n[![PyPI](https://img.shields.io/pypi/v/spotify-codegen.svg)][pypi_]\n[![Status](https://img.shields.io/pypi/status/spotify-codegen.svg)][status]\n[![Python Version](https://img.shields.io/pypi/pyversions/spotify-codegen)][python version]\n[![License](https://img.shields.io/pypi/l/spotify-codegen)][license]\n\n[![Read the documentation at https://spotify-codegen.readthedocs.io/](https://img.shields.io/readthedocs/spotify-codegen/latest.svg?label=Read%20the%20Docs)][read the docs]\n[![Tests](https://github.com/tilschuenemann/spotify-codegen/workflows/Tests/badge.svg)][tests]\n[![Codecov](https://codecov.io/gh/tilschuenemann/spotify-codegen/branch/main/graph/badge.svg)][codecov]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi_]: https://pypi.org/project/spotify-codegen/\n[status]: https://pypi.org/project/spotify-codegen/\n[python version]: https://pypi.org/project/spotify-codegen\n[read the docs]: https://spotify-codegen.readthedocs.io/\n[tests]: https://github.com/tilschuenemann/spotify-codegen/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/tilschuenemann/spotify-codegen\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\n## Features\n\nSpotify removed the feature to get a stitched image of an album / artist / track cover with their own Spotify Code. This package mimicks that behaviour and creates stitches, based on supplied\n\n- URL\n- URI\n- query\n\nIt\'s also possible to use create stitches for:\n\n- all saved albums\n- 50 followed artists (limit imposed by Spotify API)\n\n[You can also try the Streamlit showcase here.](https://tilschuenemann-showcase-showcasesstart-0ndtb3.streamlit.app/spotify_codegen)\n\n## Requirements\n\nYou\'ll need to have a Spotify Client ID & Secret in order to make API requests. Specify as environment variable like this:\n\n```console\n$ export SPOTIPY_CLIENT_ID="your_client_id"\n$ export SPOTIPY_CLIENT_ID="your_client_secret"\n```\n\n## Installation\n\nYou can install _spotify-codegen_ via [pip] from [PyPI]:\n\n```console\n$ pip install spotify-codegen\n```\n\n## Usage\n\nPlease see the [Command-line Reference] for details.\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [MIT license][license],\n_spotify-codegen_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n## Credits\n\nThis project was generated from [@cjolowicz]\'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/tilschuenemann/spotify-codegen/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/tilschuenemann/spotify-codegen/blob/main/LICENSE\n[contributor guide]: https://github.com/tilschuenemann/spotify-codegen/blob/main/CONTRIBUTING.md\n[command-line reference]: https://spotify-codegen.readthedocs.io/en/latest/usage.html\n',
    'author': 'Til Schünemann',
    'author_email': 'til.schuenemann@mailbox.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tilschuenemann/spotify-codegen',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
