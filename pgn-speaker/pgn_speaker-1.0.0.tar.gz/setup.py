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
    'version': '1.0.0',
    'description': 'Reads moves one at a time from a PGN file for practicing chess visualzation skills.',
    'long_description': 'None',
    'author': 'David Lechner',
    'author_email': 'david@lechnology.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
