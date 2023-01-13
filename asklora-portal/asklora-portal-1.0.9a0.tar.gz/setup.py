# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asklora', 'asklora.brokerage']

package_data = \
{'': ['*']}

install_requires = \
['python-dateutil>=2.8.2,<3.0.0',
 'python-dotenv>=0.20.0,<0.21.0',
 'requests>=2.28.1,<3.0.0',
 'sseclient-py>=1.7.2,<2.0.0']

setup_kwargs = {
    'name': 'asklora-portal',
    'version': '1.0.9a0',
    'description': 'portal to use various api data service',
    'long_description': '## Asklora module for ingestion data\n### drop support for RKD for this version\n\n### .env config\n`BROKER_API_URL=brokerurl`\n\n`MARKET_API_URL=market url`\n\n`BROKER_KEY=key`\n\n`BROKER_SECRET=secret`\n\n- usage\n```python\nimport asklora\n\nportal = asklora.Portal()\n\nrest = portal.get_broker_client() # get a REST client for trade, user, position , order\nmarketrest = portal.get_broker_client() # get a REST client for market data\neventclient = portal.get_event_client() # get an event client for trade, user, position, order\n```',
    'author': 'redloratech',
    'author_email': 'rede.akbar@loratechai.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
