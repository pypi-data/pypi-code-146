# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['trio_binance']

package_data = \
{'': ['*']}

install_requires = \
['dateparser>=1.1.0,<2.0.0',
 'h2>=4.1.0,<5.0.0',
 'httpx>0.20.0',
 'pytz>=2021.3,<2022.0',
 'trio-websocket>=0.9.2,<0.10.0',
 'trio>=0.20.0',
 'ujson>=5.1.0,<6.0.0']

setup_kwargs = {
    'name': 'trio-binance',
    'version': '0.2.0',
    'description': 'trio based asynchronous binance SDK',
    'long_description': '=================================\nWelcome to trio-binance\n=================================\n\nThis is an unofficial Python wrapper for the `Binance exchange REST API v3 <https://binance-docs.github.io/apidocs/spot/en>`_. I am in no way affiliated with Binance, use at your own risk.\n\nAnd this repository is forked from `python-binance <https://github.com/sammchardy/python-binance>`_, but has only async client, and works **only** with `trio <https://trio.readthedocs.io/en/stable/index.html>`_ or `trio-compatible <https://trio.readthedocs.io/en/stable/awesome-trio-libraries.html#trio-asyncio-interoperability>`_ asynchronous frameworks.\n\nSource code\n  https://github.com/halfelf/trio-binance\n\nQuick Start\n-----------\n\n`Register an account with Binance <https://accounts.binance.com/en/register?ref=10099792>`_.\n\n`Generate an API Key <https://www.binance.com/en/my/settings/api-management>`_ and assign relevant permissions.\n\n.. code:: bash\n\n    pip install trio-binance\n\n\nExample\n-------------\n\nCheck pytest file under ``tests``.\n\nDonate\n------\n\nIf this library helps, feel free to donate.\n\n- ETH: 0xf560e5F7F234307A20670ed8A5778F350a8366d1\n',
    'author': 'Shu Wang',
    'author_email': 'halfelf.ronin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/halfelf/trio-binance',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
