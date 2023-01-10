# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pacwrap']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.0,<9.0.0',
 'cmp-version>=3.0.0,<4.0.0',
 'distro>=1.8.0,<2.0.0',
 'wheel>=0.38,<0.39',
 'wtforglib>=0,<1']

entry_points = \
{'console_scripts': ['pacwrap = pacwrap.cli:main']}

setup_kwargs = {
    'name': 'pacwrap',
    'version': '0.4.0',
    'description': 'Provides single interface to several common Linux package managers.',
    'long_description': '# pacwrap\n\n[![Build Status](https://github.com/wtfo-guru/python-pacwrap/workflows/test/badge.svg?branch=main&event=push)](https://github.com/wtfo-guru/python-pacwrap/actions?query=workflow%3Atest)\n[![codecov](https://codecov.io/gh/wtfo-guru/python-pacwrap/branch/main/graph/badge.svg)](https://codecov.io/gh/wtfo-guru/python-pacwrap)\n[![Python Version](https://img.shields.io/pypi/pyversions/python-pacwrap.svg)](https://pypi.org/project/python-pacwrap/)\n[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)\n\nProvides single interface to several common Linux package managers.\n\n\n## Features\n\n- Fully typed with annotations and checked with mypy, [PEP561 compatible](https://www.python.org/dev/peps/pep-0561/)\n- Add yours!\n\n\n## Installation\n\n```bash\npip install python-pacwrap\n```\n\n\n## Usage\n\n### pacwrap help\n\n```bash\npacwrap --help\nUsage: pacwrap [OPTIONS] COMMAND [ARGS]...\n\n  Provides single interface to several common Linux package managers.\n\nOptions:\n  -d, --debug                   increment debug level\n  -o, --out TEXT                specify output file\n  -q, --quiet / --no-quiet      specify quiet mode\n  -r, --refresh / --no-refresh  specify refresh synchronized package\n                                repository data\n  -t, --test / --no-test        specify test mode\n  -v, --verbose                 increment verbosity level\n  -V, --version                 show version and exit\n  -h, --help                    Show this message and exit.\n\nCommands:\n  file       Displays package if any that include the FILE.\n  find       Searches repositories for PACKAGE.\n  info       Display information about PACKAGE.\n  install    Installs PACKAGE.\n  list       Lists files in PACKAGE or installed packages when no PACKAGE...\n  uninstall  Unistalls PACKAGE.\n```\n\n### pacwrap file help\n\n```bash\npacwrap file --help\nUsage: pacwrap file [OPTIONS] FILENAME\n\n  Displays package if any that include the FILE.\n\nOptions:\n  -h, --help  Show this message and exit.\n```\n\n### pacwrap find help\n\n```bash\npacwrap find --help\nUsage: pacwrap find [OPTIONS] PACKAGE\n\n  Searches repositories for PACKAGE.\n\nOptions:\n  --names-only / --no-names-only  specify search names only if packager\n                                  supports it\n  -h, --help                      Show this message and exit.\n```\n\n### pacwrap info help\n\n```bash\npacwrap info --help\nUsage: pacwrap info [OPTIONS] PACKAGE\n\n  Display information about PACKAGE.\n\nOptions:\n  -h, --help  Show this message and exit.\n```\n\n### pacwrap install help\n\n```bash\npacwrap install --help\nUsage: pacwrap install [OPTIONS] PACKAGE\n\n  Installs PACKAGE.\n\nOptions:\n  -h, --help  Show this message and exit.\n```\n\n### pacwrap list help\n\n```bash\npacwrap list --help\nUsage: pacwrap list [OPTIONS] [PACKAGE]\n\n  Lists files in PACKAGE or installed packages when no PACKAGE specified.\n\nOptions:\n  -h, --help  Show this message and exit.\n```\n\n### pacwrap uninstall help\n\n```bash\npacwrap uninstall --help\nUsage: pacwrap uninstall [OPTIONS] PACKAGE\n\n  Unistalls PACKAGE.\n\nOptions:\n  -h, --help  Show this message and exit.\n```\n\n## Documentation\n\n- [Stable](https://python-pacwrap.readthedocs.io/en/stable)\n\n- [Latest](https://python-pacwrap.readthedocs.io/en/latest)\n\n## License\n\n[MIT](https://github.com/wtfo-guru/python-pacwrap/blob/main/LICENSE)\n\n\n## Credits\n\nThis project was generated with [`wemake-python-package`](https://github.com/wemake-services/wemake-python-package). Current template version is: [3d9ad64bcbf7afc6bee7f2c9ea8c923d579b119c](https://github.com/wemake-services/wemake-python-package/tree/3d9ad64bcbf7afc6bee7f2c9ea8c923d579b119c). See what is [updated](https://github.com/wemake-services/wemake-python-package/compare/3d9ad64bcbf7afc6bee7f2c9ea8c923d579b119c...main) since then.\n',
    'author': 'Quien Sabe',
    'author_email': 'qs5779@mail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/wtfo-guru/pacwrap',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
