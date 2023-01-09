# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ckit', 'ckit.config', 'ckit.screens']

package_data = \
{'': ['*']}

install_requires = \
['blessed>=1.19.1,<2.0.0', 'click>=8.1.3,<9.0.0', 'pyyaml>=6.0,<7.0']

entry_points = \
{'console_scripts': ['ckit = ckit.cli:ckit']}

setup_kwargs = {
    'name': 'ckit',
    'version': '0.0.7',
    'description': 'Organize and run frequently used commands',
    'long_description': '<p align="center">\n  <img alt="ckit logo" width="460" height="300" src="https://raw.githubusercontent.com/fpgmaas/ckit/main/docs/static/ckit-logo.svg">\n</p>\n\n---\n\n[![Release](https://img.shields.io/github/v/release/fpgmaas/ckit)](https://img.shields.io/github/v/release/fpgmaas/ckit)\n[![Build status](https://img.shields.io/github/actions/workflow/status/fpgmaas/ckit/main.yml?branch=main)](https://github.com/fpgmaas/ckit/actions/workflows/main.yml?query=branch%3Amain)\n[![Supported Python versions](https://img.shields.io/pypi/pyversions/ckit)](https://pypi.org/project/ckit/)\n[![codecov](https://codecov.io/gh/fpgmaas/ckit/branch/main/graph/badge.svg)](https://codecov.io/gh/fpgmaas/ckit)\n[![PyPI - Downloads](https://img.shields.io/pypi/dm/ckit)](https://pypistats.org/packages/ckit)\n[![License](https://img.shields.io/github/license/fpgmaas/ckit)](https://img.shields.io/github/license/fpgmaas/ckit)\n\n_ckit_ is a command line utility to help you organise and quickly run frequently used commands.\n\n<p align="center">\n<img src="docs/static/ckit.gif"/>\n</p>\n\n## Quickstart\n\n### Installation\n\n_ckit_ can be installed by running\n\n```shell\npip install ckit\n```\n\nTo get started, run\n\n```shell\nckit init\n```\n\nwhich will prompt to add a `ckit/ckit.yaml` file in the user\'s home directory for global commands, and/or a `ckit.yaml` file in the current directory for commands specific to the current project. \n\nTo use _ckit_ to run any of the pre-configured commands, simply run\n\n```\nckit\n```\n\nFor more information, see the [documentation](https://fpgmaas.github.io/ckit/).\n\n## Configuration\n\n_ckit_ can look for configuration in the following two locations:\n\n- In a `ckit.yaml` file in the current directory\n- In any `.yaml` file in the the global configuration directory, which is defaulted to `~/ckit`, but which can be overridden with the environment variable `CKIT_HOME`.\n\nAn example `.yaml` file could look as follows:\n\n```yaml\ntest:\n  my-command:\n    cmd: "echo Hello! My name is: $name. My favourite fruit is: $fruit"\n    echo: false\n    args:\n      - name\n      - fruit: apple\n```\n\nWhich adds the command group `test` wth a single command called `my-command`. When `my-command` is selected to be run, _ckit_ prompts the user for `name` and `fruit` before running the command specified in `cmd`, where `fruit` is defaulted to `apple` if the user does not give any input.\n\nFor more details, see the [configuration](https://fpgmaas.github.io/ckit/configuration) section of the documentation.\n\n---\n\nRepository initiated with [fpgmaas/cookiecutter-poetry](https://github.com/fpgmaas/cookiecutter-poetry).\n',
    'author': 'Florian Maas',
    'author_email': 'fpgmaas@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/fpgmaas/ckit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
