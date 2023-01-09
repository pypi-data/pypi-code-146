# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiopvpc']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4.post0', 'async_timeout>=3.0.1']

setup_kwargs = {
    'name': 'aiopvpc',
    'version': '4.0.0',
    'description': 'Retrieval of Spanish Electricity hourly prices (PVPC)',
    'long_description': '[![PyPI Version][pypi-image]][pypi-url]\n[![pre-commit.ci Status][pre-commit-ci-image]][pre-commit-ci-url]\n[![Build Status][build-image]][build-url]\n[![Code Coverage][coverage-image]][coverage-url]\n<!-- Badges -->\n[pypi-image]: https://img.shields.io/pypi/v/aiopvpc\n[pypi-url]: https://pypi.org/project/aiopvpc/\n[pre-commit-ci-image]: https://results.pre-commit.ci/badge/github/azogue/aiopvpc/master.svg\n[pre-commit-ci-url]: https://results.pre-commit.ci/latest/github/azogue/aiopvpc/master\n[build-image]: https://github.com/azogue/aiopvpc/actions/workflows/main.yml/badge.svg\n[build-url]: https://github.com/azogue/aiopvpc/actions/workflows/main.yml\n[coverage-image]: https://codecov.io/gh/azogue/aiopvpc/branch/master/graph/badge.svg\n[coverage-url]: https://codecov.io/gh/azogue/aiopvpc\n\n# aiopvpc\n\nSimple aio library to download Spanish electricity hourly prices.\n\nMade to support the [**`pvpc_hourly_pricing`** HomeAssistant integration](https://www.home-assistant.io/integrations/pvpc_hourly_pricing/).\n\n<span class="badge-buymeacoffee"><a href="https://www.buymeacoffee.com/azogue" title="Donate to this project using Buy Me A Coffee"><img src="https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg" alt="Buy Me A Coffee donate button" /></a></span>\n\n\n## Install\n\nInstall with `pip install aiopvpc` or clone it to run tests or anything else.\n\n## Usage\n\n```python\nimport aiohttp\nfrom datetime import datetime\nfrom aiopvpc import PVPCData\n\nasync with aiohttp.ClientSession() as session:\n    pvpc_handler = PVPCData(session=session, tariff="2.0TD")\n    prices: dict = await pvpc_handler.async_update_prices(datetime.utcnow())\nprint(prices)\n```\n',
    'author': 'Eugenio Panadero',
    'author_email': 'eugenio.panadero@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/azogue/aiopvpc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
