# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bittrade_kraken_websocket',
 'bittrade_kraken_websocket.channels',
 'bittrade_kraken_websocket.channels.models',
 'bittrade_kraken_websocket.connection',
 'bittrade_kraken_websocket.development',
 'bittrade_kraken_websocket.events',
 'bittrade_kraken_websocket.events.models',
 'bittrade_kraken_websocket.messages',
 'bittrade_kraken_websocket.messages.filters',
 'bittrade_kraken_websocket.operators']

package_data = \
{'': ['*']}

install_requires = \
['bittrade-kraken-rest>=0.12.3,<0.13.0',
 'expression>=4.2.2,<5.0.0',
 'orjson>=3.8.3,<4.0.0',
 'pydantic>=1.10.4,<2.0.0',
 'reactivex>=4.0.4,<5.0.0',
 'websocket-client>=1.4.2,<2.0.0']

setup_kwargs = {
    'name': 'bittrade-kraken-websocket',
    'version': '0.3.3',
    'description': 'Reactive Websocket for Kraken',
    'long_description': '# Kraken Websocket\n\n[NOT RELEASED] This is very much a work in progress, despite being on pypi.\nMost things might be wrongly documented; API **will** change\n\n## Features\n\n- Reconnect with incremental backoff (per Kraken\'s recommendation)\n- Automatically reset subscription for private feeds when sequence is out of whack\n- request/response factories e.g. `add_order_factory` make websocket events feel like calling an API\n- ... but provides more info than a simple request/response; \n  for instance, `add_order` goes through each stage submitted->pending->open or canceled, \n  emitting a notification at each stage\n\n## Installing\n\n`pip install bittrade-kraken-websocket` or `poetry add bittrade-kraken-websocket`\n\n## General considerations\n\n### Observables/Reactivex\n\nThe whole library is build with [Reactivex](https://rxpy.readthedocs.io/en/latest/).\n\nThough Observables seem complicated at first, they are the best way to handle - and (synchronously) test - complex situations that arise over time, like an invalid sequence of messages or socket disconnection and backoff reconnects.\n\nFor simple use cases, they are also rather easy to use as shown in the [examples](./examples) folder or in the Getting Started below\n\n### Concurrency\n\nInternally the library uses threads.\nFor your main program you don\'t have to worry about threads; you can block the main thread.\n\n## Getting started\n\n### Connect to the public feeds\n\n```python\nfrom bittrade_kraken_websocket import public_websocket_connection, subscribe_ticker\nfrom bittrade_kraken_websocket.operators import keep_messages_only, filter_new_socket_only\n\n# Prepare connection - note, this is a ConnectableObservable, so it will only trigger connection when we call its ``connect`` method\nsocket_connection = public_websocket_connection()\n# Prepare a feed with only "real" messages, dropping things like status update, heartbeat, etc…\nmessages = socket_connection.pipe(\n    keep_messages_only(),\n)\nsocket_connection.pipe(\n    filter_new_socket_only(),\n    subscribe_ticker(\'USDT/USD\', messages)\n).subscribe(\n    print, print, print  # you can do anything with the messages; here we simply print them out\n)\nsocket_connection.connect()\n```\n\n_(This script is complete, it should run "as is")_\n\n\n## Logging\n\nWe use Python\'s standard logging.\nYou can modify what logs you see as follows:\n\n```\nlogging.getLogger(\'bittrade_kraken_websocket\').addHandler(logging.StreamHandler())\n```\n\n## Private feeds\n\nSimilar to [bittrade-kraken-rest](https://github.com/TechSpaceAsia/bittrade-kraken-rest), this library attempts to get as little access to sensitive information as possible.\n\nCurrently, you need to set the token onto the `EnhancedWebsocket`; this means we have no access to your Api key and secret.\nSince the token is connection based and can\'t be reused, this protects you as much as Kraken\'s current authentication method allows.\n\nIn the future we might even let you code your own `send_json` method instead.\n\nSee `examples/private_subscription.py` for an example of implementation\n\n```python\nnew_sockets = connection.pipe(\n    filter_new_socket_only(),\n    operators.map(add_token),\n    operators.share(),\n)\n```\n\n## Examples\n\nMost examples in the `examples` folder make use of the `development` module helpers and the rich logging. You will need to install the dependencies from the `rich` group to use them:\n\n`poetry add bittrade_kraken_websocket -E rich`',
    'author': 'mat',
    'author_email': 'matt@techspace.asia',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/TechSpaceAsia/bittrade-kraken-websocket',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
