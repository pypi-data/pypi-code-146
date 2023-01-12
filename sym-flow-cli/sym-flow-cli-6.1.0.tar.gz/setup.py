# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sym',
 'sym.flow.cli',
 'sym.flow.cli.code_generation',
 'sym.flow.cli.code_generation.approval',
 'sym.flow.cli.commands',
 'sym.flow.cli.commands.bots',
 'sym.flow.cli.commands.config',
 'sym.flow.cli.commands.debug',
 'sym.flow.cli.commands.domains',
 'sym.flow.cli.commands.resources',
 'sym.flow.cli.commands.services',
 'sym.flow.cli.commands.services.click',
 'sym.flow.cli.commands.services.hooks',
 'sym.flow.cli.commands.tokens',
 'sym.flow.cli.commands.users',
 'sym.flow.cli.helpers',
 'sym.flow.cli.helpers.login',
 'sym.flow.cli.models',
 'sym.flow.cli.tests',
 'sym.flow.cli.tests.commands',
 'sym.flow.cli.tests.commands.bots',
 'sym.flow.cli.tests.commands.config',
 'sym.flow.cli.tests.commands.debug',
 'sym.flow.cli.tests.commands.resources',
 'sym.flow.cli.tests.commands.services',
 'sym.flow.cli.tests.commands.services.hooks',
 'sym.flow.cli.tests.commands.tokens',
 'sym.flow.cli.tests.commands.users',
 'sym.flow.cli.tests.factories',
 'sym.flow.cli.tests.helpers',
 'sym.flow.cli.tests.helpers.login',
 'sym.flow.cli.tests.models']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'analytics-python>=1.3.1,<2.0.0',
 'auth0-python>=3.23.1,<4.0.0',
 'boto3>=1.16.20,<2.0.0',
 'click>=8.0.0,<9.0.0',
 'immutables>=0.14,<0.15',
 'inflection>=0.5.1,<0.6.0',
 'inquirer>=2.7.0,<3.0.0',
 'mistune<2.0.0',
 'pkce>=1.0,<2.0',
 'prompt-toolkit>=3.0.21,<4.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'pytest-factoryboy>=2.1.0,<3.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'semver>=2.13.0,<3.0.0',
 'sentry-sdk>=1.0.0,<2.0.0',
 'sym-shared-cli>=0.2.4,<0.3.0',
 'tabulate>=0.8.7,<0.9.0',
 'validators>=0.18.1,<0.19.0',
 'xattr>=0.9.7,<0.10.0']

entry_points = \
{'console_scripts': ['symflow = sym.flow.cli.symflow:symflow']}

setup_kwargs = {
    'name': 'sym-flow-cli',
    'version': '6.1.0',
    'description': "Sym's Official CLI for Implementers",
    'long_description': '# sym-flow-cli\n\nThis is the official CLI for [Sym](https://symops.com/) Implementers. Check out the docs [here](https://docs.symops.com/docs/install-sym-flow).\n',
    'author': 'SymOps, Inc.',
    'author_email': 'pypi@symops.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://symops.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
