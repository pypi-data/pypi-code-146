# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['apiclarity']

package_data = \
{'': ['*']}

install_requires = \
['pydantic[dotenv]>=1.10.4,<2.0.0', 'requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['pytest = pytest:main']}

setup_kwargs = {
    'name': 'apiclarity',
    'version': '0.2.0',
    'description': 'Client python package for interaction with APIClarity.',
    'long_description': '# Python APIClarity client\n\n[![GitHub Actions status](https://github.com/openclarity/python-apiclarity-client/workflows/Test/badge.svg)](https://github.com/openclarity/python-apiclarity-client/actions)\n[![Code style: Black](https://img.shields.io/badge/code%20style-Black-000000.svg)](https://github.com/psf/black)\n\nPython client package for [APIClarity](https://github.com/openclarity/apiclarity) interaction.\n\n[APIClarity](https://github.com/openclarity/apiclarity) is a modular tool that addresses several aspects of API Security, focusing specifically on [OpenAPI based APIs](https://spec.openapis.org/oas/latest.html). APIClarity approaches API Security in 2 different ways:\n\n  * Captures all API traffic in a given environment and performs a set of security analysis to discover all potential security problems with detected APIs\n  * Actively tests API endpoints to detect security issues in the implementation of such APIs.\n\n## Usage\n\nThe `ClientSession` class is based on [requests.Session]() and can be used similarly. To configure the session, provide a `ClientSettings` object:\n\n```python\nfrom apiclarity import ClientSession, ClientSettings\n\napiclarity_session = ClientSession(ClientSettings(\n    apiclarity_endpoint="http://apiclarity",\n    default_timeout=(9.0, 3.0),\n))\napiInfo = apiclarity_session.getInventory()\nfor api in apiInfo.items:\n    print(f"received: {api}\\n")\n```\n\nThe settings can also be retrieved from the environment during creation of the `ClientSettings` object, given here with the defaults:\n\n```shell\nAPICLARITY_ENDPOINT="http://apiclarity:8080"\nTELEMETRY_ENDPOINT="http://apiclarity:9000"\nHEALTH_ENDPOINT="http://apiclarity:8081"\n```\n\n# Contributing\nPull requests and bug reports are welcome. Please see [CONTRIBUTING.md](https://github.com/openclarity/python-apiclarity-client/blob/main/CONTRIBUTING.md).\n\n# License\nThe code is released under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0).\n',
    'author': 'Jeff Napper',
    'author_email': 'jenapper@cisco.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/openclarity/python-apiclarity-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
