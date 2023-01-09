# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pianopy']

package_data = \
{'': ['*']}

install_requires = \
['mingus>=0.6.1,<0.7.0',
 'numpy>=1.24.1,<2.0.0',
 'pygame>=2.1.2,<3.0.0',
 'python-rtmidi>=1.4.9,<2.0.0']

entry_points = \
{'console_scripts': ['pianopy = pianopy.__main__:main']}

setup_kwargs = {
    'name': 'pianopy',
    'version': '0.0.2',
    'description': 'A python library/application to play, compose and interface with virtual and real pianos using MIDI.',
    'long_description': '# pianopy\nA python library/application to play, compose and interface with virtual and \nreal pianos using MIDI.\n\n## Run tests, build, publish\n1. Run the unittests:  \n`make test`\n2. Build the package as a wheel:  \n`make build`\n3. Publish the package to pypi\n`make publish`\n\n## Development setup\n1. Make sure prerequisites are installed\n2. Clone the git repo:  \n`git clone https://github.com/PeterPyPan/pianopy`\n3. Use make to setup the dev environment:\n```\n# This sets up a venv in ./.venv using poetry and installs the pre-commit hooks.  \nmake setup\n```\n\n## Prerequisites\n1. Install `poetry`  \nVerify the poetry installation using:  \n`poetry --version`  \nInstallation instructions: https://python-poetry.org/docs/#installation.\n\n2. Install `make`\nVerify the make installation using:  \n`make --version`  \n\n```\n# Installation for OSX\n# remove previous installation of command line tools\nrm -rf /Library/Developer/CommandLineTools/\n# install command line tools\nxcode-select --install\n# setup command line tools\nsudo xcode-select --switch /Library/Developer/CommandLineTools/\n```\n',
    'author': 'PeterPyPan',
    'author_email': 'PeterPyPanGitHub@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/PeterPyPan/pianopy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
