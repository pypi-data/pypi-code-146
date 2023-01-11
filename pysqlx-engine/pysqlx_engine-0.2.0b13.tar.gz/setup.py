# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysqlx_engine', 'pysqlx_engine._core']

package_data = \
{'': ['*']}

install_requires = \
['Pygments>=2.14.0,<3.0.0',
 'pydantic>=1.10.4,<2.0.0',
 'pysqlx-core>=0.1.31,<0.2.0',
 'typing-extensions>=4.3.0,<5.0.0']

setup_kwargs = {
    'name': 'pysqlx-engine',
    'version': '0.2.0b13',
    'description': 'Async and Sync SQL Engine for Python, with support for MySQL, PostgreSQL, SQLite and Microsoft SQL Server.',
    'long_description': '# PySQLXEngine\n\n<p align="center">\n  <a href="/"><img src="https://carlos-rian.github.io/pysqlx-engine/img/logo-text3.png" alt="PySQLXEngine Logo"></a>\n</p>\n<p align="center">\n    <em>PySQLXEngine, a minimalist SQL engine</em>\n</p>\n\n<p align="center">\n<a href="https://github.com/carlos-rian/pysqlx-engine/actions?query=workflow%3ATest+event%3Apush+branch%3Amain" target="_blank">\n    <img src="https://github.com/carlos-rian/pysqlx-engine/workflows/Test/badge.svg?event=push&branch=main" alt="Test">\n</a>\n<a href="https://app.codecov.io/gh/carlos-rian/pysqlx-engine" target="_blank">\n    <img src="https://img.shields.io/codecov/c/github/carlos-rian/pysqlx-engine?color=%2334D058" alt="Coverage">\n</a>\n<a href="https://pypi.org/project/pysqlx-engine" target="_blank">\n    <img src="https://img.shields.io/pypi/v/pysqlx-engine?color=%2334D058&label=pypi%20package" alt="Package version">\n</a>\n<a href="https://pypi.org/project/pysqlx-engine" target="_blank">\n    <img src="https://img.shields.io/pypi/pyversions/pysqlx-engine.svg?color=%2334D058" alt="Supported Python versions">\n</a>\n</p>\n\n---\n\n**Documentation**: <a href="https://carlos-rian.github.io/pysqlx-engine/" target="_blank">https://carlos-rian.github.io/pysqlx-engine/</a>\n\n**Source Code**: <a href="https://github.com/carlos-rian/pysqlx-engine" target="_blank">https://github.com/carlos-rian/pysqlx-engine</a>\n\n---\n\nPySQLXEngine supports the option of sending **Raw SQL** to your database.\n\nThe PySQLXEngine is a minimalist [SQL Engine](https://github.com/carlos-rian/pysqlx-engine).\n\nThe PySQLXEngine was created and thought to be minimalistic, but very efficient. The core is write in [**Rust**](https://www.rust-lang.org), making communication between Databases and [**Python**](https://python-poetry.org) more efficient.\n\nAll SQL executed using PySQLXEngine is atomic; only one instruction is executed at a time. Only the first one will be completed if you send an Insert and a select. This is one of the ways to handle SQL ingestion. As of version **0.2.0**, PySQLXEngine supports transactions, where you can control [`BEGIN`](https://learn.microsoft.com/en-us/sql/t-sql/language-elements/begin-end-transact-sql?view=sql-server-ver16), [`COMMIT`](https://www.geeksforgeeks.org/difference-between-commit-and-rollback-in-sql), [ `ROLLBACK` ](https://www.geeksforgeeks.org/difference-between-commit-and-rollback-in-sql), [`ISOLATION LEVEL`](https://levelup.gitconnected.com/understanding-isolation-levels-in-a-database-transaction-af78aea3f44), etc. as you wish.\n\n\n> **NOTE**:\n    Minimalism is not the lack of something, but having exactly what you need.\n    PySQLXEngine aims to expose an easy interface for you to communicate with the database in a simple, intuitive way and with good help through documentation, autocompletion, typing, and good practices.\n---\n\nDatabase Support:\n\n* [`SQLite`](https://www.sqlite.org/index.html)\n* [`PostgreSQL`](https://www.postgresql.org/)\n* [`MySQL`](https://www.mysql.com/)\n* [`Microsoft SQL Server`](https://www.microsoft.com/sql-server)\n\nOS Support:\n\n* [`Linux`](https://pt.wikipedia.org/wiki/Linux)\n* [`MacOS`](https://pt.wikipedia.org/wiki/Macos)\n* [`Windows`](https://pt.wikipedia.org/wiki/Microsoft_Windows)\n\n\n## Installation\n\n\nPIP\n\n```console\n$ pip install pysqlx-engine\n```\n\nPoetry\n\n```console\n$ poetry add pysqlx-engine\n```\n\n## Async Example\n\nCreate a `main.py` file and add the code examples below.\n\n```python\nfrom pysqlx_engine import PySQLXEngine\n\nasync def main():\n    db = PySQLXEngine(uri="sqlite:./db.db")\n    await db.connect()\n\n    await db.execute(sql="CREATE TABLE IF NOT EXISTS users (id INT PRIMARY KEY, name TEXT, age INT)")\n    await db.execute(sql="INSERT INTO users (name, age) VALUES (\'Rian\', \'28\')")\n    await db.execute(sql="INSERT INTO users (name, age) VALUES (\'Carlos\', \'29\')")\n\n    rows = await db.query(sql="SELECT * FROM users")\n\n    print(rows)\n\nimport asyncio\nasyncio.run(main())\n```\n\n## Sync Example\n\nCreate a `main.py` file and add the code examples below.\n\n```python\nfrom pysqlx_engine import PySQLXEngineSync\n\ndef main():\n    db = PySQLXEngineSync(uri="sqlite:./db.db")\n    db.connect()\n\n    db.execute(sql="CREATE TABLE IF NOT EXISTS users (id INT PRIMARY KEY, name TEXT, age INT)")\n    db.execute(sql="INSERT INTO users (name, age) VALUES (\'Rian\', \'28\')")\n    db.execute(sql="INSERT INTO users (name, age) VALUES (\'Carlos\', \'29\')")\n\n    rows = db.query(sql="SELECT * FROM users")\n\n    print(rows)\n\n# running the code\nmain()\n```\n\nRunning the code using the terminal\n\n\n```console\n$ python3 main.py\n```\nOutput\n\n```python\n[\n    BaseRow(id=1, name=\'Rian\', age=28),  \n    BaseRow(id=2, name=\'Carlos\', age=29)\n]\n```\n',
    'author': 'Carlos Rian',
    'author_email': 'crian.rian@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://carlos-rian.github.io/pysqlx-engine',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
