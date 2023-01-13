# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['raumo_data_tools', 'raumo_data_tools.chart_tools']

package_data = \
{'': ['*'], 'raumo_data_tools': ['configs/*', 'secrets/*']}

install_requires = \
['influxdb-client>=1.28.0,<2.0.0',
 'pandas>=1.4.0,<2.0.0',
 'sqlalchemy>=1.4,<2.0']

setup_kwargs = {
    'name': 'raumo-data-tools',
    'version': '0.1.6',
    'description': 'Package containing core functions for data ETL workloads.',
    'long_description': '# data_toolbox\nPackage containing core functions for data ETL workloads.\n\n# Installation\nInside poetry project:\n`poetry add raumo-data-tools`\n\nWith pip:\n`pip install raumo-data-tools`\n\n# Package contents\n### Config handler\nReading configuration files for databases and servers\n\n### influx writer\nFunctions for writing to InfluxDB\n\n### pipelines\nSimple pipeline class\n',
    'author': 'Tanja Klopper',
    'author_email': 't.klopper@raumobil.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/raumobil/data_toolbox',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
