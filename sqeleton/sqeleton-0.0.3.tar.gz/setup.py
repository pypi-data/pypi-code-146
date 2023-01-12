# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqeleton', 'sqeleton.abcs', 'sqeleton.databases', 'sqeleton.queries']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1,<9.0',
 'dsnparse',
 'rich',
 'runtype>=0.2.6,<0.3.0',
 'toml>=0.10.2,<0.11.0']

extras_require = \
{'clickhouse': ['clickhouse-driver'],
 'duckdb': ['duckdb>=0.6.0,<0.7.0'],
 'mysql': ['mysql-connector-python==8.0.29'],
 'postgresql': ['psycopg2'],
 'presto': ['presto-python-client'],
 'snowflake': ['snowflake-connector-python>=2.7.2,<3.0.0', 'cryptography'],
 'trino': ['trino>=0.314.0,<0.315.0'],
 'tui': ['textual>=0.9.1,<0.10.0', 'textual-select']}

entry_points = \
{'console_scripts': ['sqeleton = sqeleton.__main__:main']}

setup_kwargs = {
    'name': 'sqeleton',
    'version': '0.0.3',
    'description': 'Python library for querying SQL databases',
    'long_description': '# Sqeleton\n\n**Under construction!**\n\nSqeleton is a Python library for querying SQL databases.\n\nIt consists of -\n\n- A fast and concise query builder, inspired by PyPika and SQLAlchemy\n\n- A modular database interface, with drivers for a long list of SQL databases.\n\nIt is comparable to other libraries such as SQLAlchemy or PyPika, in terms of API and intended audience. However there are several notable ways in which it is different.\n\n### Built for performance\n\n- Multi-threaded by default -\n    The same connection object can be used from multiple threads without any additional setup.\n\n- No ORM\n    ORMs are easy and familiar, but they encourage bad and slow code. Sqeleton is designed to push the compute to SQL.\n\n- Fast query-builder\n    Sqeleton\'s query-builder runs about 4 times faster than SQLAlchemy\'s.\n\n### Type-aware\n\nSqeleton has a built-in feature to query the schemas of the databases it supports.\n\nThis feature can be also used to inform the query-builder, either as an alternative to defining the tables yourself, or to validate that your definitions match the actual schema.\n\nThe schema is used for validation when building expressions, making sure the names are correct, and that the data-types align.\n\n### Multi-database access\n\nSqeleton is designed to work with several databases at the same time. Its API abstracts away as many implementation details as possible.\n\nDatabases we support:\n\n- PostgreSQL >=10\n- MySQL\n- Snowflake\n- BigQuery\n- Redshift\n- Oracle\n- Presto\n- Databricks\n- Trino\n- Clickhouse\n- Vertica\n- DuckDB >=0.6\n- SQLite (coming soon)\n\n\n### Documentation\n\n[Read the docs!](https://sqeleton.readthedocs.io)\n\n### Basic usage\n\n```python\nfrom sqeleton import connect, table, this\n\n# Create a new database connection\nddb = connect("duckdb://:memory:")\n\n# Define a table with one int column\ntbl = table(\'my_list\', schema={\'item\': int})\n\n# Make a bunch of queries\nqueries = [\n    # Create table \'my_list\'\n    tbl.create(),\n\n    # Insert 100 numbers\n    tbl.insert_rows([x] for x in range(100)),\n\n    # Get the sum of the numbers\n    tbl.select(this.item.sum())\n]\n# Query in order, and return the last result as an int\nresult = ddb.query(queries, int)    \n\n# Prints: Total sum of 0..100 = 4950\nprint(f"Total sum of 0..100 = {result}")\n```\n\n\n# TODO\n\n- Transactions\n\n- Indexes\n\n- Date/time expressions\n\n- Window functions\n\n## Possible plans for the future (not determined yet)\n\n- Cache the compilation of repetitive queries for even faster query-building\n\n- Compile control flow, functions\n\n- Define tables using type-annotated classes (SQLModel style)\n',
    'author': 'Erez Shinan',
    'author_email': 'erezshin@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/datafold/sqeleton',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
