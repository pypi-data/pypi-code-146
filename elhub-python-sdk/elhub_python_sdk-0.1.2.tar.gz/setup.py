# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['elhub_sdk', 'tests', 'tests.tests_examples']

package_data = \
{'': ['*']}

install_requires = \
['mkdocs-material-extensions>=1.0.3,<2.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'zeep[xmlsec]>=4.1.0,<5.0.0']

extras_require = \
{':extra == "dev"': ['tox>=3.26.0,<4.0.0',
                     'virtualenv>=20.16.5,<21.0.0',
                     'pip>=22.2.2,<23.0.0',
                     'twine>=4.0.1,<5.0.0',
                     'bump2version>=1.0.1,<2.0.0',
                     'toml>=0.10.2,<0.11.0',
                     'pre-commit>=2.20.0,<3.0.0'],
 ':extra == "doc"': ['mkdocs>=1.3.1,<2.0.0',
                     'mkdocstrings[python-legacy]>=0.19.0,<0.20.0',
                     'mkdocs-material>=8.5.3,<9.0.0',
                     'mkdocs-autorefs>=0.4.1,<0.5.0',
                     'mkdocs-include-markdown-plugin>=3.8.1,<4.0.0'],
 ':extra == "test"': ['black>=22.8.0,<23.0.0',
                      'isort>=5.10.1,<6.0.0',
                      'flake8>=5.0.4,<6.0.0',
                      'mypy>=0.971,<0.972',
                      'pytest>=7.1.3,<8.0.0',
                      'flake8-docstrings>=1.6.0,<2.0.0',
                      'pytest-cov>=3.0.0,<4.0.0']}

setup_kwargs = {
    'name': 'elhub-python-sdk',
    'version': '0.1.2',
    'description': 'Non official Python SDK for ElHub API.',
    'long_description': '# Non official Python SDK for ElHub API\n\n[![pypi](https://img.shields.io/pypi/v/elhub-python-sdk.svg)](https://pypi.org/project/elhub-python-sdk/)\n[![python](https://img.shields.io/pypi/pyversions/elhub-python-sdk.svg)](https://pypi.org/project/elhub-python-sdk/)\n[![Build Status](https://github.com/bkkas/elhub-python-sdk/actions/workflows/dev.yml/badge.svg)](https://github.com/bkkas/elhub-python-sdk/actions/workflows/dev.yml)\n\n\nWelcome to the **non official** Open Source Python SDK for ElHub API.\n\nThe objective is to create an SDK that will improve the speed and quality of the development against the ElHub API,\nsupported by the community.\n\nWe are at a very early stage of development, we welcome all the contributions in any kind, please have a look\nat the following if you are interested.\n\n\n## Contributing\n\n* Documentation: <https://bkkas.github.io/elhub-python-sdk>\n* GitHub: <https://github.com/bkkas/elhub-python-sdk>\n* GitHub: <https://github.com/bkkas/elhub-python-sdk/discussions>\n* PyPI: <https://pypi.org/project/elhub-python-sdk/>\n\n\n## License\n\nGPL-3.0\n\n\n## Credits\n\nThis package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and\nthe [waynerv/cookiecutter-pypackage](https://github.com/waynerv/cookiecutter-pypackage) project template.\n',
    'author': 'Volte',
    'author_email': 'jesus.condon@eviny.no',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bkkas/elhub-python-sdk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8.2,<4.0',
}


setup(**setup_kwargs)
