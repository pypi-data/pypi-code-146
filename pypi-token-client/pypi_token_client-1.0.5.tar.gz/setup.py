# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypi_token_client', 'pypi_token_client.utils']

package_data = \
{'': ['*']}

install_requires = \
['keyring>=23.13.1,<24.0.0',
 'playwright>=1.29,<2.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['pypi-token-client = pypi_token_client.cli:cli_main']}

setup_kwargs = {
    'name': 'pypi-token-client',
    'version': '1.0.5',
    'description': 'Library and CLI tool for creating PyPI project tokens',
    'long_description': '# pypi-token-client\n\n[![pipeline status](https://gitlab.com/smheidrich/pypi-token-client/badges/main/pipeline.svg?style=flat-square)](https://gitlab.com/smheidrich/pypi-token-client/-/commits/main)\n[![docs](https://img.shields.io/badge/docs-online-brightgreen?style=flat-square)](https://smheidrich.gitlab.io/pypi-token-client/)\n[![pypi](https://img.shields.io/pypi/v/pypi-token-client)](https://pypi.org/project/pypi-token-client/)\n[![supported python versions](https://img.shields.io/pypi/pyversions/pypi-token-client)](https://pypi.org/project/pypi-token-client/)\n\nLibrary and CLI tool for creating and managing PyPI project tokens.\n\n## Purpose\n\nPyPI allows the creation of per-project tokens but\n[doesn\'t](https://github.com/pypi/warehouse/issues/6396) currently have an API\nto do so. While integration with CI providers is\n[planned](https://github.com/pypi/warehouse/issues/6396#issuecomment-1345585291),\napparently there is\n[no plan](https://github.com/pypi/warehouse/issues/6396#issuecomment-1345667940)\nfor an API that would allow one to create tokens from a local development\nmachine.\n\nThis tool seeks to provide a client exposing this functionality anyway by\nwhatever means necessary.\n\n## Operating principle\n\nBecause there is no API and I\'m also too lazy to try and figure out the exact\nsequence of HTTP requests one would have to make to simulate what happens when\nrequesting tokens on the PyPI website, for now this tool just uses\n[Playwright](https://playwright.dev/python/) to automate performing the\nnecessary steps in an *actual* browser.\n\nThis might be overkill and brittle but it works for now 🤷\n\n## Installation\n\nTo install from PyPI:\n\n```bash\npip3 install pypi-token-client\n```\n\nYou\'ll also have to install the required Playwright browsers (currently just\nChromium):\n\n```bash\nplaywright install chromium\n```\n\n## Command-line tool usage\n\nTo create a token `yourtokenname` for your PyPI project `yourproject`:\n\n```bash\npypi-token-client create --project yourproject yourtokenname\n```\n\nThere are more commands - please refer to the docs.\n\n## Usage as a library\n\nBasic example script:\n\n```python\nimport asyncio\nfrom os import getenv\n\nfrom pypi_token_client import (\n  async_pypi_token_client, SingleProject, PypiCredentials\n)\n\ncredentials = PypiCredentials(getenv("PYPI_USER"), getenv("PYPI_PASS"))\n\nasync def main() -> str:\n  async with async_pypi_token_client(credentials) as session:\n      token = await session.create_token(\n          "my token",\n          SingleProject("my-project"),\n      )\n  return token\n\ntoken = asyncio.run(main())\n\nprint(token)\n```\n\n## More information\n\nFor more detailed usage information and the API reference, refer to\n[the documentation](https://smheidrich.gitlab.io/pypi-token-client/).\n\n## License\n\nMIT License, see `LICENSE` file.\n',
    'author': 'smheidrich',
    'author_email': 'smheidrich@weltenfunktion.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://smheidrich.gitlab.io/pypi-token-client/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
