# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aioeapi', 'asynceapi']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.3,<0.24.0']

setup_kwargs = {
    'name': 'aio-eapi',
    'version': '0.4.0',
    'description': 'Arista EOS API asyncio client',
    'long_description': '# Arista EOS API asyncio Client\n\nThis repository contains an Arista EOS asyncio client.\n\n### Quick Example\n\nThie following shows how to create a Device instance and run a list of\ncommands.\n\nDevice will use HTTPS transport by default.  The Device instance supports the\nfollowing initialization parameters:\n\n   * `host` - The device hostname or IP address\n   * `username` - The login username\n   * `password` - The login password\n   * `proto` - *(Optional)* Choose either "https" or "http", defaults to "https"\n   * `port` - *(Optional)* Chose the protocol port to override proto default\n\nThe Device class inherits directly from httpx.AsyncClient.  As such, the Caller\ncan provide any initialization parameters.  The above specific parameters are\nall optional.\n\n```python\nimport json\nfrom aioeapi import Device\n\nusername = \'dummy-user\'\npassword = \'dummy-password\'\n\nasync def run_test(host):\n    dev = Device(host=host, username=username, password=password)\n    res = await dev.cli(commands=[\'show hostname\', \'show version\'])\n    json.dumps(res)\n```\n',
    'author': 'Jeremy Schulman',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
