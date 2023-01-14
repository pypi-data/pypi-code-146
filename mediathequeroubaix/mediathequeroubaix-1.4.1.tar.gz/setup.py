# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mediathequeroubaix',
 'mediathequeroubaix.auth',
 'mediathequeroubaix.get_loans',
 'mediathequeroubaix.renew']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.2,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'returns>=0.19.0,<0.20.0',
 'rich>=12.6.0,<13.0.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['mediathequeroubaix = mediathequeroubaix.app:app']}

setup_kwargs = {
    'name': 'mediathequeroubaix',
    'version': '1.4.1',
    'description': 'Client for the library of Roubaix (Médiathèque Roubaix)',
    'long_description': '<p align="center" width="100%">\n  <img src="doc/banner.png" alt="MediathequeRoubaix.py"/>\n</p>\n\n# Python CLI for the library of Roubaix (Médiathèque Roubaix)\n\n[![PyPI](https://img.shields.io/pypi/v/mediathequeroubaix?style=flat-square)](https://pypi.python.org/pypi/mediathequeroubaix/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mediathequeroubaix?style=flat-square)](https://pypi.python.org/pypi/mediathequeroubaix/)\n[![PyPI - License](https://img.shields.io/pypi/l/mediathequeroubaix?style=flat-square)](https://pypi.python.org/pypi/mediathequeroubaix/)\n\n---\n\n**Releases**: [https://github.com/tomsquest/mediathequeroubaix.py/releases](https://github.com/tomsquest/mediathequeroubaix.py/releases)\n\n**Source Code**: [https://github.com/tomsquest/mediathequeroubaix.py](https://github.com/tomsquest/mediathequeroubaix.py)\n\n**PyPI**: [https://pypi.org/project/mediathequeroubaix/](https://pypi.org/project/mediathequeroubaix/)\n\n---\n\n<!-- START doctoc generated TOC please keep comment here to allow auto update -->\n<!-- DON\'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->\n## Table of Contents\n\n- [Features](#features)\n  - [Display your loans](#display-your-loans)\n  - [Renew your loans](#renew-your-loans)\n- [Usage](#usage)\n  - [Install](#install)\n  - [Create an initial, sample configuration](#create-an-initial-sample-configuration)\n  - [Display the current configuration](#display-the-current-configuration)\n  - [List the loans](#list-the-loans)\n  - [Renew the loans](#renew-the-loans)\n- [Why I am doing this](#why-i-am-doing-this)\n- [Changelog](#changelog)\n- [Installation](#installation)\n- [Development](#development)\n  - [Releasing](#releasing)\n- [Credits](#credits)\n\n<!-- END doctoc generated TOC please keep comment here to allow auto update -->\n\n## Features\n\nMédiathèqueRoubaix.py is a client for the **libray of Roubaix**, [mediathequederoubaix.fr](http://www.mediathequederoubaix.fr/).\n\n<p align="center" width="100%">\n  <img src="doc/mr_homepage.png" alt="Screenshot mediathequederoubaix.fr"/>\n</p>\n\n### Display your loans\n\nRunning `mediathequeroubaix loans list` will:\n\n1. Get the **list of your loans** and their due date\n2. ...for **many cardholders**\n3. and check the **next return date** for each of your card\n\n### Renew your loans\n\nRunning `mediathequeroubaix loans renew` will:\n\n1. Renew **automatically** all loans\n2. ...for **many cardholders**\n3. and print the **new due date** of the loans\n\n## Usage\n\n### Install\n\n```shell\npip install mediathequederoubaix\n```\n\n### Create an initial, sample configuration\n\n`config create` makes a sample configuration in `$HOME/.config/mediathequederoubaix/config.json` and display the content of the file.  \nThe configuration is initialized with a sample but fake user.\n\n```shell\nmediathequeroubaix config create\n```\n\n<p align="center" width="100%">\n  <img src="doc/cli_config_create.png" alt="Screenshot CLI config create"/>\n</p>\n\n### Display the current configuration\n\n`config show` displays the current configuration.\n\n```shell\nmediathequeroubaix config show\n```\n\n<p align="center" width="100%">\n  <img src="doc/cli_config_show.png" alt="Screenshot CLI config show"/>\n</p>\n\n### List the loans\n\n`loans list` show the list of loans for the users.\n\n```shell\nmediathequeroubaix loans list\n```\n\n<p align="center" width="100%">\n  <img src="doc/cli_loans_list.png" alt="Screenshot CLI loans list"/>\n</p>\n\n### Renew the loans\n\n`loans renew` renew the list of loans for the users and display the new loans.\n\n```shell\nmediathequeroubaix loans renew\n```\n\n<p align="center" width="100%">\n  <img src="doc/cli_loans_renew.png" alt="Screenshot CLI loans renew"/>\n</p>\n\n## Why I am doing this\n\nI created this project to:\n\n1. Learn **Functional Programing**\n2. Learn **typed** and **modern** Python\n3. Be able to quickly list and renew my loans (especially when you have many cards)\n\n## Changelog\n\nSee [CHANGELOG.md](CHANGELOG.md)\n\n## Installation\n\n```sh\npip install mediathequeroubaix\n```\n\n## Development\n\n* Clone this repository\n* Requirements:\n    * [Poetry](https://python-poetry.org/)\n    * Python 3.10\n* Create a virtual environment and install the dependencies\n\n```sh\npoetry install\n```\n\n* Activate the virtual environment\n\n```sh\npoetry shell\n```\n\n* Install Pre-commit\n\n```sh\npre-commit install\n```\n\n* Test\n\n```sh\npytest\n```\n\n* Check everything in one go\n\n```sh\npre-commit run --all-files\n```\n\n### Releasing\n\nTrigger the [Draft release workflow](https://github.com/tomsquest/mediathequeroubaix.py/actions/workflows/draft_release.yml)\n(press _Run workflow_). This will update the changelog & version and create a GitHub release which is in _Draft_ state.\n\nFind the draft release from the\n[GitHub releases](https://github.com/tomsquest/mediathequeroubaix.py/releases) and publish it. When\na release is published, it\'ll trigger [release](https://github.com/tomsquest/mediathequeroubaix.py/blob/master/.github/workflows/release.yml) workflow which creates PyPI\nrelease.\n\n## Credits\n\n- Background and color from [PrettySnap](https://prettysnap.app/)\n- Python project bootstrapped using [Wolt template](https://github.com/woltapp/wolt-python-package-cookiecutter)\n- Functional library is [Returns from DRY-Python](https://github.com/dry-python/returns)\n- Tables look great thanks to [Textualize\'s Rich](https://github.com/Textualize/rich)\n- CLI screenshot pimped with [ShowCode.app](https://showcode.app)\n',
    'author': 'Thomas Queste',
    'author_email': 'tom@tomsquest.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://tomsquest.github.io/mediathequeroubaix.py',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10.0,<3.11.0',
}


setup(**setup_kwargs)
