# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['schematic_db',
 'schematic_db.db_config',
 'schematic_db.query_store',
 'schematic_db.rdb',
 'schematic_db.rdb_queryer',
 'schematic_db.rdb_updater',
 'schematic_db.schema',
 'schematic_db.synapse']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'SQLAlchemy-Utils>=0.38.3,<0.39.0',
 'SQLAlchemy>=1.4.39,<2.0.0',
 'black>=22.6.0,<23.0.0',
 'mypy>=0.982,<0.983',
 'mysqlclient>=2.1.1,<3.0.0',
 'networkx>=2.8.6,<3.0.0',
 'pandas>=1.4.3,<2.0.0',
 'pdoc>=12.1.0,<13.0.0',
 'psycopg2>=2.9.5,<3.0.0',
 'pylint>=2.15.4,<3.0.0',
 'pytest-mock>=3.10.0,<4.0.0',
 'requests>=2.28.1,<3.0.0',
 'synapseclient>=2.6.0,<3.0.0',
 'tenacity>=8.1.0,<9.0.0']

setup_kwargs = {
    'name': 'schematic-db',
    'version': '0.0.4',
    'description': '',
    'long_description': 'None',
    'author': 'andrewelamb',
    'author_email': 'andrewelamb@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
