# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['requests_oidc']

package_data = \
{'': ['*']}

install_requires = \
['requests-oauthlib>=1.3.1,<2.0.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'requests-oidc',
    'version': '0.1.4',
    'description': '',
    'long_description': 'Requests-OIDC\n=================\n\n.. inclusion-marker-do-not-remove\n\nImplements a simple single-function API for creating a requests ``Session`` that\nmanages your OIDC-discovered OAuth2 session for you.\n\n::\n\n   pip install requests-oidc\n\n\n.. list-table::\n\n   * - Package\n     - |pypi| |license| |py status| |formats| |python| |py impls| |downloads|\n   * - build\n     - |checks| |rtd build| |coverage|\n   * - Git\n     - |last commit| |commit activity| |commits since| |issues| |prs|\n\n.. |pypi| image:: https://img.shields.io/pypi/v/requests-oidc\n   :target: https://pypi.org/project/requests-oidc/\n   :alt: PyPI\n   \n.. |downloads| image:: https://img.shields.io/pypi/dm/requests-oidc\n   :target: https://pypistats.org/packages/requests-oidc\n   :alt: PyPI - Downloads\n\n.. |formats| image:: https://img.shields.io/pypi/format/requests-oidc\n   :target: https://pypi.org/project/requests-oidc/\n   :alt: PyPI - Format\n\n.. |py status| image:: https://img.shields.io/pypi/status/requests-oidc\n   :target: https://pypi.org/project/requests-oidc/\n   :alt: PyPI - Status\n\n.. |py impls| image:: https://img.shields.io/pypi/implementation/requests-oidc\n   :target: https://pypi.org/project/requests-oidc/\n   :alt: PyPI - Implementation\n\n.. |python| image:: https://img.shields.io/pypi/pyversions/requests-oidc\n   :target: https://pypi.org/project/requests-oidc/\n   :alt: PyPI - Python Version\n\n.. |license| image:: https://img.shields.io/github/license/tsweeney-dust/requests-oidc\n   :target: https://github.com/tsweeney-dust/requests-oidc\n   :alt: GitHub\n\n.. |checks| image:: https://img.shields.io/github/checks-status/tsweeney-dust/requests-oidc/main?logo=github\n   :target: https://github.com/tsweeney-dust/requests-oidc\n   :alt: GitHub branch checks state\n\n.. |rtd build| image:: https://img.shields.io/readthedocs/requests-oidc\n   :target: https://requests-oidc.readthedocs.io/en/latest/?badge=latest\n   :alt: Read the Docs\n\n.. |coverage| image:: https://coveralls.io/repos/github/tsweeney-dust/requests-oidc/badge.svg?branch=main\n   :target: https://coveralls.io/github/tsweeney-dust/requests-oidc?branch=main\n   :alt: Coverage\n\n.. |last commit| image:: https://img.shields.io/github/last-commit/tsweeney-dust/requests-oidc\n   :target: https://github.com/tsweeney-dust/requests-oidc\n   :alt: GitHub last commit\n\n.. |commit activity| image:: https://img.shields.io/github/commit-activity/m/tsweeney-dust/requests-oidc\n   :target: https://github.com/tsweeney-dust/requests-oidc\n   :alt: GitHub commit activity\n\n.. |commits since| image:: https://img.shields.io/github/commits-since/tsweeney-dust/requests-oidc/latest\n   :target: https://github.com/tsweeney-dust/requests-oidc\n   :alt: GitHub commits since latest release (by SemVer)\n\n.. |issues| image:: https://img.shields.io/github/issues/tsweeney-dust/requests-oidc\n   :target: https://github.com/tsweeney-dust/requests-oidc/issues\n   :alt: GitHub issues\n\n.. |prs| image:: https://img.shields.io/github/issues-pr/tsweeney-dust/requests-oidc\n   :target: https://github.com/tsweeney-dust/requests-oidc/pulls\n   :alt: GitHub pull requests',
    'author': 'Tristan Sweeney',
    'author_email': 'tsweeney@dustidentity.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tsweeney-dust/requests-oidc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
