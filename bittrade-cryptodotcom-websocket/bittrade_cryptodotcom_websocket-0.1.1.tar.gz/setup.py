# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bittrade_cryptodotcom_websocket',
 'bittrade_cryptodotcom_websocket.channels',
 'bittrade_cryptodotcom_websocket.channels.models',
 'bittrade_cryptodotcom_websocket.connection',
 'bittrade_cryptodotcom_websocket.development',
 'bittrade_cryptodotcom_websocket.events',
 'bittrade_cryptodotcom_websocket.events.models',
 'bittrade_cryptodotcom_websocket.messages',
 'bittrade_cryptodotcom_websocket.messages.filters',
 'bittrade_cryptodotcom_websocket.models',
 'bittrade_cryptodotcom_websocket.operators',
 'bittrade_cryptodotcom_websocket.rest']

package_data = \
{'': ['*']}

install_requires = \
['ccxt>=2.6.5,<3.0.0',
 'expression>=4.2.2,<5.0.0',
 'orjson>=3.8.3,<4.0.0',
 'pydantic>=1.10.4,<2.0.0',
 'reactivex>=4.0.4,<5.0.0',
 'returns>=0.19.0,<0.20.0',
 'websocket-client>=1.4.2,<2.0.0']

setup_kwargs = {
    'name': 'bittrade-cryptodotcom-websocket',
    'version': '0.1.1',
    'description': 'Reactive Websocket for Crypto.com',
    'long_description': '# Crypto.com Websocket\n\n[NOT RELEASED] This is very much a work in progress, despite being on pypi.\nMost things might be wrongly documented; API **will** change\n\n## Features\n\n- Reconnect with incremental backoff \n- Respond to ping\n- request/response factories e.g. `add_order_factory` make websocket events feel like calling an API\n- ... but provides more info than a simple request/response; \n  for instance, `add_order` goes through each stage submitted->pending->open or canceled, \n  emitting a notification at each stage\n\n## Installing\n\n`pip install bittrade-cryptodotcom-websocket` or `poetry add bittrade-cryptodotcom-websocket`\n\n## General considerations\n\n### Observables/Reactivex\n\nThe whole library is build with [Reactivex](https://rxpy.readthedocs.io/en/latest/).\n\nThough Observables seem complicated at first, they are the best way to handle - and (synchronously) test - complex situations that arise over time, like an invalid sequence of messages or socket disconnection and backoff reconnects.\n\nFor simple use cases, they are also rather easy to use as shown in the [examples](./examples) folder or in the Getting Started below\n\n### Concurrency\n\nInternally the library uses threads.\nFor your main program you don\'t have to worry about threads; you can block the main thread.\n\n## Getting started\n\n### Connect to the public feeds\n\n```python\nfrom bittrade_cryptodotcom_websocket import public_websocket_connection, subscribe_ticker\nfrom bittrade_cryptodotcom_websocket.operators import keep_messages_only, filter_new_socket_only\n\n# Prepare connection - note, this is a ConnectableObservable, so it will only trigger connection when we call its ``connect`` method\nsocket_connection = public_websocket_connection()\n# Prepare a feed with only "real" messages, dropping things like status update, heartbeat, etc…\nmessages = socket_connection.pipe(\n    keep_messages_only(),\n)\nsocket_connection.pipe(\n    filter_new_socket_only(),\n    subscribe_ticker(\'USDT/USD\', messages)\n).subscribe(\n    print, print, print  # you can do anything with the messages; here we simply print them out\n)\nsocket_connection.connect()\n```\n\n_(This script is complete, it should run "as is")_\n\n\n## Logging\n\nWe use Python\'s standard logging.\nYou can modify what logs you see as follows:\n\n```\nlogging.getLogger(\'bittrade_cryptodotcom_websocket\').addHandler(logging.StreamHandler())\n```\n\n## Private feeds\n\nSimilar to [bittrade-kraken-rest](https://github.com/TechSpaceAsia/bittrade-kraken-rest), this library attempts to get as little access to sensitive information as possible.\n\nThis means that you\'ll need to implement the signature token yourself. The library never has access to your API secret.\n\nSee `examples/private_subscription.py` for an example of implementation but it is generally as simple as:\n\n```python\nauthenticated_sockets = connection.pipe(\n    filter_new_socket_only(),\n    operators.map(add_token),\n    operators.share(),\n)\n```\n\n## Examples\n\nMost examples in the `examples` folder make use of the `development` module helpers and the rich logging. You will need to install the dependencies from the `rich` group to use them:\n\n`poetry add bittrade_cryptodotcom_websocket -E rich`',
    'author': 'mat',
    'author_email': 'matt@techspace.asia',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/TechSpaceAsia/bittrade-cryptodotcom-websocket',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
