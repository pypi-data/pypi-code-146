# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['toolbox',
 'toolbox.common',
 'toolbox.sets.business',
 'toolbox.sets.dw',
 'toolbox.sets.hash',
 'toolbox.sets.pdf']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'ocrmypdf>=14.0.1,<15.0.0',
 'pdf2docx>=0.5.6,<0.6.0',
 'pylint>=2.15.5,<3.0.0',
 'pytest>=7.2,<8.0',
 'rich>=12.6.0,<13.0.0',
 'tomli>=2.0.1,<3.0.0',
 'typer[all]>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['test = toolbox.scripts:test',
                     'toolbox = toolbox.cli:main']}

setup_kwargs = {
    'name': 'atelier-toolbox',
    'version': '1.0.1',
    'description': 'Tools for various automations 🧰',
    'long_description': '# atelier-toolbox\n\n![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/mihaichris/atelier-toolbox/build.yml)\n![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/mihaichris/atelier-toolbox/test.yml?label=test)\n[![Issues](https://img.shields.io/github/issues/mihaichris/atelier-toolbox)](https://github.com/mihaichris/atelier-toolbox/issues)\n[![License](https://img.shields.io/github/license/mihaichris/atelier-toolbox)](https://github.com/mihaichris/atelier-toolbox/blob/main/LICENSE)\n[![Version](https://img.shields.io/github/v/tag/mihaichris/atelier-toolbox)](https://github.com/mihaichris/atelier-toolbox/blob/main/LICENSE)\n[![Python Version](https://img.shields.io/pypi/pyversions/atelier-toolbox)](https://pypi.org/project/atelier-toolbox/)\n\n## Description\n\nTools for various automations 🧰.\n\n## Installation\n\nYou can install the Toolbox from [PyPI](https://pypi.org/):\n\n```python\npython -m pip install atelier-toolbox\n```\nThe package is supported on Python 3.10 and above.\n\n\n## How to use\n\n```python\nUsage: toolbox [OPTIONS] COMMAND [ARGS]...\n\n╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮\n│ --install-completion          Install completion for the current shell.                                                                                                                                   │\n│ --show-completion             Show completion for the current shell, to copy it or customize the installation.                                                                                            │\n│ --help                        Show this message and exit.                                                                                                                                                 │\n╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\n╭─ Commands ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮\n│ business                                                  Business CLI Tool                                                                                                                               │\n│ dw                                                        Download CLI Tool                                                                                                                               │\n│ hash                                                      Hashing Files CLI Tool                                                                                                                          │\n│ pdf                                                       PDF CLI Tool                                                                                                                                    │\n╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\n```\n\n## CHANGELOG\n Please refer to [CHANGELOG.md](https://github.com/mihaichris/toolbox/blob/main/CHANGELOG.md)\n\n## License\n[MIT](https://opensource.org/licenses/MIT)\n',
    'author': 'Mihai',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mihaichris/atelier-toolbox',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
