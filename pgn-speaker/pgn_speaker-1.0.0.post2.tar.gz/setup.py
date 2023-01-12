# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pgn_speaker']

package_data = \
{'': ['*']}

install_requires = \
['chess>=1.9.4,<2.0.0']

extras_require = \
{':sys_platform == "darwin"': ['pyobjc-framework-avfoundation>=9.0.1,<10.0.0'],
 ':sys_platform == "win32"': ['windows-curses>=2.3.1,<3.0.0',
                              'winsdk>=1.0.0b7,<2.0.0']}

entry_points = \
{'console_scripts': ['pgn-speaker = pgn_speaker.cli:main']}

setup_kwargs = {
    'name': 'pgn-speaker',
    'version': '1.0.0.post2',
    'description': 'Reads moves one at a time from a PGN file for practicing chess visualzation skills.',
    'long_description': '# PGN Speaker\n\nCommand line program that speaks moves from a PGN file.\n\nThis is intended to assist in visualization exercises as described in\nhttps://nextlevelchess.blog/improve-your-visualization/\n\n## Running the program\n\n`pgn-speaker` is a Python program and therefore requires a Python runtime.\nInstead of using `pip` to get the package, it is recommended to use [pipx].\nThis ensures you are always running the latest version of `pgn-speaker`.\n\nAfter installing `pipx` run the following command where `$PGN` is the path to\na PGN file saved on your computer.\n\n    pipx run pgn-speaker $PGN\n\nIf `pipx` is not in your `PATH`, you may need to run it as a module instead:\n\n    python3 -m pipx ...\n\nOr if using the Python Launcher for Windows:\n\n    py -3 -m pipx ...\n\n[pipx]: https://pypa.github.io/pipx/\n\n## System requirements\n\n- Python >= 3.10\n- Windows >= 10\n- macOS >= 10.14\n',
    'author': 'David Lechner',
    'author_email': 'david@lechnology.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/dlech/python-pgn-speaker',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
