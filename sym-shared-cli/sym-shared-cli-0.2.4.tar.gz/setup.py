# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shared',
 'shared.cli',
 'shared.cli.data',
 'shared.cli.helpers',
 'shared.cli.helpers.config',
 'shared.cli.tests',
 'shared.cli.tests.helpers']

package_data = \
{'': ['*']}

install_requires = \
['analytics-python>=1.3.1,<2.0.0',
 'boto3>=1.16.20,<2.0.0',
 'click-option-group>=0.5.1,<0.6.0',
 'click>=8.0.4,<9.0.0',
 'colorama<0.4.4',
 'cryptography==3.4.8',
 'immutables>=0.14,<0.15',
 'portalocker>=2.0.0,<3.0.0',
 'requests>=2.25,<3.0',
 'semver>=2.13.0,<3.0.0',
 'sentry-sdk>=1.0.0,<2.0.0',
 'validators>=0.18.1,<0.19.0']

setup_kwargs = {
    'name': 'sym-shared-cli',
    'version': '0.2.4',
    'description': "Sym's CLI shared library",
    'long_description': '# sym-shared-cli\n\nThis is the shared library for [Sym](https://symops.com/) command line tools. Check out the docs [here](https://docs.symops.com/docs/install-sym-flow).\n',
    'author': 'SymOps, Inc.',
    'author_email': 'pypi@symops.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://symops.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
