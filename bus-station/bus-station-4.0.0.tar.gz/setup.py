# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['bus_station',
 'bus_station.command_terminal',
 'bus_station.command_terminal.bus',
 'bus_station.command_terminal.bus.asynchronous',
 'bus_station.command_terminal.bus.asynchronous.distributed',
 'bus_station.command_terminal.bus.synchronous',
 'bus_station.command_terminal.bus.synchronous.distributed',
 'bus_station.command_terminal.bus_engine',
 'bus_station.command_terminal.middleware',
 'bus_station.command_terminal.middleware.implementations',
 'bus_station.command_terminal.registry',
 'bus_station.event_terminal',
 'bus_station.event_terminal.bus',
 'bus_station.event_terminal.bus.asynchronous',
 'bus_station.event_terminal.bus.asynchronous.distributed',
 'bus_station.event_terminal.bus.synchronous',
 'bus_station.event_terminal.bus_engine',
 'bus_station.event_terminal.middleware',
 'bus_station.event_terminal.middleware.implementations',
 'bus_station.event_terminal.registry',
 'bus_station.passengers',
 'bus_station.passengers.passenger_record',
 'bus_station.passengers.reception',
 'bus_station.passengers.serialization',
 'bus_station.query_terminal',
 'bus_station.query_terminal.bus',
 'bus_station.query_terminal.bus.synchronous',
 'bus_station.query_terminal.bus.synchronous.distributed',
 'bus_station.query_terminal.bus_engine',
 'bus_station.query_terminal.middleware',
 'bus_station.query_terminal.middleware.implementations',
 'bus_station.query_terminal.registry',
 'bus_station.query_terminal.serialization',
 'bus_station.shared_terminal',
 'bus_station.shared_terminal.broker_connection',
 'bus_station.shared_terminal.broker_connection.connection_parameters',
 'bus_station.shared_terminal.bus_stop_resolver',
 'bus_station.shared_terminal.engine',
 'bus_station.shared_terminal.engine.runner',
 'bus_station.shared_terminal.factories',
 'bus_station.tracking_terminal',
 'bus_station.tracking_terminal.mappers',
 'bus_station.tracking_terminal.mappers.sqlalchemy',
 'bus_station.tracking_terminal.models',
 'bus_station.tracking_terminal.repositories',
 'bus_station.tracking_terminal.repositories.implementations',
 'bus_station.tracking_terminal.repositories.implementations.pymongo',
 'bus_station.tracking_terminal.repositories.implementations.sqlalchemy',
 'bus_station.tracking_terminal.trackers']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy==1.4.29',
 'jsonrpcclient>=4.0.2,<5.0.0',
 'jsonrpcserver>=5.0.6,<6.0.0',
 'kombu==5.2.2',
 'pymongo==4.0.1',
 'pypendency>=0.1.0,<0.2.0',
 'redis==4.1.0',
 'requests>=2.27.1,<3.0.0',
 'rpyc==5.0.1']

setup_kwargs = {
    'name': 'bus-station',
    'version': '4.0.0',
    'description': 'A python bus station',
    'long_description': '# Bus station\nPython bus pattern implementation\n',
    'author': 'DeejayRevok',
    'author_email': 'seryi_one@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10.0,<3.11.0',
}


setup(**setup_kwargs)
