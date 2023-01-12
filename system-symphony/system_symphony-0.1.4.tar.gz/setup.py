# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['process_parser', 'supercollider']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'psutil>=5.9.4,<6.0.0', 'python-osc>=1.8.0,<2.0.0']

entry_points = \
{'console_scripts': ['system-symphony = process_parser.main:main']}

setup_kwargs = {
    'name': 'system-symphony',
    'version': '0.1.4',
    'description': 'Explore the sonic world of your computer.',
    'long_description': '# system-symphony\n\nExplore the sonic world of your computer.\n\n`system-syphony` sonifies your computer by transforming its running processes into synthesized sounds.  \n\n## Installation\n### Preqrequisites\n1. Install [Supercollider](https://supercollider.github.io/downloads) on your current platform.\n2. Make sure `sclang` is added to system PATH.\n    - **Mac**: `sclang` may be stored at `/Applications/SuperCollider.app/Contents/MacOS/` or `/Applications/SuperCollider/SuperCollider.app/Contents/MacOS/`\n    - **Windows**: `sclang` is likely stored at: `C:\\Program Files\\SuperCollider-<version>`\n### Installing Locally\n1. Run `pip install .` in `src/system-symphony` directory\n\n\n### Installing through pypi\n1. Run `pip install system-symphony`\n\n## Usage\n\n```\nUsage: system-symphony [OPTIONS]\n\n  Explore the sonic world of your computer. Associated supercollider file must\n  be running.\n\nOptions:\n  --poll-rate INTEGER  How fast to poll processes in ms\n  --no-sc              Do not launch the supercollider process.\n  --help               Show this message and exit.\n\n```\n\n\n',
    'author': 'Darwin',
    'author_email': 'darwin78913@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/dsmaugy/the-sounds-of-processes',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
