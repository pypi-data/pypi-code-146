# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysignalclijsonrpc']

package_data = \
{'': ['*']}

install_requires = \
['jmespath>=1.0.1,<2.0.0',
 'packaging>=21.3,<22.0',
 'python-magic>=0.4.27,<0.5.0',
 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'pysignalclijsonrpc',
    'version': '23.1.1',
    'description': 'Python API client for signal-cli JSON-RPC',
    'long_description': "# pysignalclijsonrpc - Python API client for signal-cli JSON-RPC\n\nPython client for [signal-cli 0.11.5+](https://github.com/AsamK/signal-cli/blob/master/CHANGELOG.md#0115---2022-11-07) native HTTP endpoint for JSON-RPC methods.\n\n## Documentation\n\nSee https://pysignalclijsonrpc.readthedocs.io/\n\n## Support\n\nIf you like what i'm doing, you can support me via [Paypal](https://paypal.me/morph027), [Ko-Fi](https://ko-fi.com/morph027) or [Patreon](https://www.patreon.com/morph027).\n",
    'author': 'Stefan Heitmüller',
    'author_email': 'stefan.heitmueller@gmx.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/morph027/pysignalclijsonrpc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
