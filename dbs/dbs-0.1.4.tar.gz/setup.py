# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dbs']

package_data = \
{'': ['*']}

install_requires = \
['databases[aiosqlite]>=0.6.1,<0.7.0',
 'pydantic>=1.10.4,<2.0.0',
 'rich>=12.6.0,<13.0.0',
 'typer>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['query = dbs.query:app']}

setup_kwargs = {
    'name': 'dbs',
    'version': '0.1.4',
    'description': '',
    'long_description': "[![image](https://img.shields.io/pypi/v/package_name.svg)](https://pypi.org/project/package_name)\n\n# DBS\n\n## Getting started\nInstallation:\n```\npip install dbs\n```\n\nRun with:\n```\npython3 -m dbs.query\n```\n\n## Using\nExecute one query:\n```\npython3 -m dbs.query 'sqlite://:inmemory:' 'sqls/select.sql'\n```\n\nPipe commands together:\n```\nexport DB_HOST='sqlite://:inmemory:'\npython3 -m dbs.query $DB_HOST 'sqls/create.sql'\npython3 -m dbs.query $DB_HOST 'sqls/select_table_1.sql' | python3 -m dbs.query $DB_HOST 'sqls/select_table_2.sql'\n```\n\n# How to contribute\n\n",
    'author': 'yeger00',
    'author_email': 'yeger00@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
