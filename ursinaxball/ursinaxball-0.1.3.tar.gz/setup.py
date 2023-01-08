# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ursinaxball',
 'ursinaxball.modules',
 'ursinaxball.modules.physics',
 'ursinaxball.modules.player',
 'ursinaxball.modules.systems',
 'ursinaxball.objects',
 'ursinaxball.objects.base',
 'ursinaxball.stadiums']

package_data = \
{'': ['*']}

install_requires = \
['msgpack>=1.0.4,<2.0.0', 'numpy>=1.23.5,<2.0.0', 'ursina==5.0.0']

setup_kwargs = {
    'name': 'ursinaxball',
    'version': '0.1.3',
    'description': '',
    'long_description': '# Ursinaxball\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nUrsinaxball is a Python clone of the game [HaxBall](https://www.haxball.com) developed with the ursina game engine.\n\n## Requirements\n\n- Python == 3.10\n\n## Installation\n\nInstall the library via pip:\n\n```bash\npip install ursinaxball\n```\n\nOnce installed, copy the example.py file and run it. The game should be playing fine!\n',
    'author': 'Wazarr',
    'author_email': 'jeje_04@live.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
