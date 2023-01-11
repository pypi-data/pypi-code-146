# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pomace', 'pomace.tests']

package_data = \
{'': ['*'], 'pomace.tests': ['cassettes/*']}

install_requires = \
['beautifulsoup4>=4.8.2,<5.0.0',
 'bullet>=2.2,<3.0',
 'cleo>=2.0,<3.0',
 'datafiles>=2.0,<3.0',
 'fake-useragent>=1.1,<2.0',
 'faker>=15',
 'flask-api>=3.0,<4.0',
 'gitman>=3.3,<4.0',
 'inflection>=0.5.1,<0.6.0',
 'ipdb>=0.13.9,<0.14.0',
 'ipython>=8.4,<9.0',
 'minilog>=2.0,<3.0',
 'nest-asyncio>=1.5.5,<2.0.0',
 'parse>=1.14,<2.0',
 'selenium>=4.4,<5.0',
 'splinter>=0.18.1,<0.19.0',
 'universal-startfile',
 'us>=2.0.2,<3.0.0',
 'webdriver_manager>=3.8.5,<4.0.0',
 'zipcodes>=1.2,<2.0']

extras_require = \
{':platform_machine != "armv7l"': ['playwright>=1.24,<2.0']}

entry_points = \
{'console_scripts': ['pomace = pomace.cli:application.run']}

setup_kwargs = {
    'name': 'pomace',
    'version': '0.12',
    'description': 'Dynamic page objects for browser automation.',
    'long_description': "# Pomace\n\nDynamic page objects for browser automation.\n\n[![Unix Build Status](https://img.shields.io/github/actions/workflow/status/jacebrowning/pomace/main.yml?branch=main&label=unix)](https://github.com/jacebrowning/pomace/actions)\n[![Windows Build Status](https://img.shields.io/appveyor/ci/jacebrowning/pomace/main.svg?label=window)](https://ci.appveyor.com/project/jacebrowning/pomace)\n[![Coverage Status](https://img.shields.io/codecov/c/gh/jacebrowning/pomace)](https://codecov.io/gh/jacebrowning/pomace)\n[![PyPI Version](https://img.shields.io/pypi/v/pomace.svg)](https://pypi.org/project/pomace)\n[![PyPI License](https://img.shields.io/pypi/l/pomace.svg)](https://pypi.org/project/pomace)\n\n## Quick Start\n\nOpen **Terminal.app** in macOS and paste:\n\n```shell\npython3 -m pip install --upgrade pomace && python3 -m pomace run\n```\n\nor if you have Homebrew:\n\n```shell\nbrew install pipx; pipx run --no-cache pomace run\n```\n\n## Full Demo\n\nIf you're planning to run Pomace multiple times, install it with [pipx](https://pipxproject.github.io/pipx/) first:\n\n```shell\npipx install pomace\n```\n\nor get the latest version:\n\n```shell\npipx upgrade pomace\n```\n\nThen download some site models:\n\n```shell\npomace clone https://github.com/jacebrowning/pomace-twitter.com\n```\n\nAnd launch the application:\n\n```shell\npomace run twitter.com\n```\n\n# Usage\n\nInstall this library directly into an activated virtual environment:\n\n```shell\npip install pomace\n```\n\nor add it to your [Poetry](https://poetry.eustace.io/) project:\n\n```shell\npoetry add pomace\n```\n",
    'author': 'Jace Browning',
    'author_email': 'jacebrowning@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pypi.org/project/pomace',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
