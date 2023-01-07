# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['yumemi']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=22.1,<23.0',
 'click>=8.1,<9.0',
 'cryptography>=38.0,<39.0',
 'rhash-rhash>=1.1,<2.0']

entry_points = \
{'console_scripts': ['yumemi = yumemi.cli:main']}

setup_kwargs = {
    'name': 'yumemi',
    'version': '2.0.0',
    'description': 'AniDB library and simple CLI client.',
    'long_description': 'Yumemi\n======\n\nAniDB API library for Python and simple CLI client to add files to mylist.\n\n\nInstallation\n------------\n\nI recommend using pipx_ to install the CLI client ::\n\n    pipx install yumemi\n\nCLI requires LibRHash library. It is recommended to install LibRHash using your\nsystem package manager, see RHash_ project page.\n\n.. _pipx: https://pypa.github.io/pipx/\n.. _RHash: https://pypi.org/project/rhash-Rhash/\n',
    'author': 'Filip Pobořil',
    'author_email': 'tsuki@fpob.cz',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/fpob-dev/yumemi',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
