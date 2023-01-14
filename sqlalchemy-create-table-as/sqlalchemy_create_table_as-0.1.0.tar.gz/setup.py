# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqlalchemy_create_table_as']

package_data = \
{'': ['*']}

install_requires = \
['sqlalchemy>=1.0.0']

setup_kwargs = {
    'name': 'sqlalchemy-create-table-as',
    'version': '0.1.0',
    'description': 'module provide *create table as* statement',
    'long_description': '# "Create Table As" form for SQLAlchemy\n\nAdd `create table as` construct to SQLalchemy\n\n## Usage\n\nExamples:\n```python\n>>> from sqlalchemy import *\n>>> from sqlalchemy_create_table_as import *\n>>> str(\n...     CreateTableAs(\n...         table(\'new_table\'), \n...         select(column(\'f1\'), column(\'f2\')).select_from(table(\'old_table\'))\n...         )\n... )\n\'CREATE TABLE new_table AS SELECT f1, f2 \\nFROM old_table\'\n \n>>> t = Table(\'old_table\', MetaData(), Column(\'f1\'), Column(\'f2\'))\n\n>>> str(CreateTableAs(table(\'new_table\'), select(t)))\n>>> \'CREATE TABLE new_table AS SELECT old_table.f1, old_table.f2 \\nFROM old_table\'\n```\n\n## Installation\n\n...',
    'author': 'Nedosekov Ivan',
    'author_email': 'ivan-nedd@mail.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
