# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['libretro_scummvm_playlist']

package_data = \
{'': ['*']}

install_requires = \
['typer[all]>=0.5.0,<0.6.0']

entry_points = \
{'console_scripts': ['libretro-scummvm-playlist = '
                     'libretro_scummvm_playlist.__main__:main']}

setup_kwargs = {
    'name': 'libretro-scummvm-playlist',
    'version': '2.2.6',
    'description': 'libretro scummvm playlist builder',
    'long_description': None,
    'author': 'i30817',
    'author_email': 'i30817@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
