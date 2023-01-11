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
    'version': '0.2.1',
    'description': 'Async and Sync SQL Engine for Python, with support for MySQL, PostgreSQL, SQLite and Microsoft SQL Server.',
    'long_description': '# PySQLXEngine\n\n<p align="center">\n  <a href="/"><img src="https://carlos-rian.github.io/pysqlx-engine/img/logo-text3.png" alt="PySQLXEngine Logo"></a>\n</p>\n<p align="center">\n    <em>PySQLXEngine, a minimalist SQL engine</em>\n</p>\n\n<p align="center">\n<a href="https://github.com/carlos-rian/pysqlx-engine/actions?query=workflow%3ATest+event%3Apush+branch%3Amain" target="_blank">\n    <img src="https://github.com/carlos-rian/pysqlx-engine/workflows/Test/badge.svg?event=push&branch=main" alt="Test">\n</a>\n<a href="https://app.codecov.io/gh/carlos-rian/pysqlx-engine" target="_blank">\n    <img src="https://img.shields.io/codecov/c/github/carlos-rian/pysqlx-engine?color=%2334D058" alt="Coverage">\n</a>\n<a href="https://pypi.org/project/pysqlx-engine" target="_blank">\n    <img src="https://img.shields.io/pypi/v/pysqlx-engine?color=%2334D058&label=pypi%20package" alt="Package version">\n</a>\n<a href="https://pypi.org/project/pysqlx-engine" target="_blank">\n    <img src="https://img.shields.io/pypi/pyversions/pysqlx-engine.svg?color=%2334D058" alt="Supported Python versions">\n</a>\n</p>\n\n---\n\n**Documentation**: <a href="https://carlos-rian.github.io/pysqlx-engine/" target="_blank">https://carlos-rian.github.io/pysqlx-engine/</a>\n\n**Source Code**: <a href="https://github.com/carlos-rian/pysqlx-engine" target="_blank">https://github.com/carlos-rian/pysqlx-engine</a>\n\n---\n\nPySQLXEngine supports the option of sending **raw sql** to your database.\n\nThe PySQLXEngine is a minimalist **Async and Sync** SQL engine. Currently this lib only supports *async and sync programming*.\n\nThe PySQLXEngine was created and thought to be minimalistic, but very efficient. The core is write in Rust, making communication between database and Python more efficient.\n\n\n\nDatabase Support:\n\n* `SQLite`\n* `PostgreSQL`\n* `MySQL`\n* `Microsoft SQL Server`\n\nOS Support:\n\n* `Linux`\n* `MacOS`\n* `Windows`\n\n## Installation\n\n\nPIP\n\n```console\n$ pip install pysqlx-engine\n```\n\nPoetry\n\n```console\n$ poetry add pysqlx-engine\n```\n\n\n\n## Async Example\n\n* Create `main.py` file.\n\n```python\nimport asyncio\n\nfrom pysqlx_engine import PySQLXEngine\n\nuri = "sqlite:./db.db"\ndb = PySQLXEngine(uri=uri)\n\nasync def main():\n    await db.connect()\n    rows = await db.query(sql="select 1 as number")\n    print(rows)\n\nasyncio.run(main())\n```\n\n## Sync Example\n\n* Create `main.py` file.\n\n```python\nfrom pysqlx_engine import PySQLXEngineSync\n\nuri = "sqlite:./db.db"\ndb = PySQLXEngineSync(uri=uri)\n\ndef main():\n    db.connect()\n    rows = db.query(sql="select 1 as number")\n    print(rows)\n\nmain()\n```\n\n* Run it\n\n<div class="termy">\n\n```console\n$ python3 main.py\n\n[BaseRow(number=1)]\n```\n</div>\n',
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
