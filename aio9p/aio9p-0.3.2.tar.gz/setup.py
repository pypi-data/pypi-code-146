# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aio9p', 'aio9p.dialect', 'aio9p.dialect.client', 'aio9p.example']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aio9p',
    'version': '0.3.2',
    'description': '',
    'long_description': '# aio9p\n\nAsyncio-based bindings for the 9P protocol. Work in progress.\n\nWorking examples for the 9P2000 and 9P2000.u dialects are implemented in\naio9p.example .\n\n## Features\n\n* 9P2000 client and server\n* 9P2000.u client and server\n* Transports: TCP, domain sockets\n\n## TODO\n\n### Documentation\n- Client examples.\n\n### Features\n- Support for the 9P2000.L dialect\n\n### Testing\n- Significantly expanded unit testing\n- Expanded integration tests\n- Benchmarking\n',
    'author': 'florpe',
    'author_email': 'jens.krewald@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
