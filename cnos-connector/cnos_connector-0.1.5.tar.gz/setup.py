# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cnosdb_connector']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cnos-connector',
    'version': '0.1.5',
    'description': 'CnosDB Python Client',
    'long_description': '# CnosDB Python Connector\n\nCnosDB Python Connector repository contains the Python client library for the [CnosDB](https://github.com/cnosdb/cnosdb). cnosdb_connector adapted for PEP249.\n\n## Installation\n\nuse pip install it from pypi, **Python 3.6** or later is required.\n\n```\npip install cnos-connector\n```\n\nThen import the package:\n\n```\nimport cnosdb_connector\n```\n\n## Getting Started\n\n#### Query use SQL\n\n```python\nfrom cnosdb_connector import connect\n\nconn = connect(url="http://127.0.0.1:31007/", user="root", password="")\nresp = conn.execute("SHOW DATABASES")\nprint(resp)\n```\n\n#### Query use interface\n\n```python\nfrom cnosdb_connector import connect\n\nconn = connect(url="http://127.0.0.1:31007/", user="root", password="")\nconn.create_database("air")\nresp = conn.list_database()\nprint(resp)\n```\n\n#### Query use PEP-249\n\n```python\nfrom cnosdb_connector import connect\n\nconn = connect(url="http://127.0.0.1:31007/", user="root", password="")\ncursor = conn.cursor()\n\ncursor.execute("SHOW DATABASES")\nresp = cursor.fetchall()\nprint(resp)\n```\n\n#### Query use pandas\n\n```python\nimport pandas as pd\nfrom cnosdb_connector import connect\n\nconn = connect(url="http://127.0.0.1:31007/", user="root", password="")\n\nresp = pd.read_sql("SHOW DATABASES", conn)\nprint(resp)\n```\n\n#### Write use LineProtocol\n\n```python\nfrom cnosdb_connector import connect\n\nline0 = "test_insert,ta=a1,tb=b1 fa=1,fb=2 1"\nline1 = "test_insert,ta=a1,tb=b1 fa=3,fb=4 2"\nline2 = "test_insert,ta=a1,tb=b1 fa=5,fb=6 3"\n\nconn = connect(url="http://127.0.0.1:31007/", user="root", password="")\n\nconn.create_database_with_ttl("test_database", "100000d")\nconn.switch_database("test_database")\n\nconn.write_lines([line0, line1, line2])\n\nresp = conn.execute("SELECT * FROM test_insert;")\nprint(resp)\n```\n\n#### Write use SQL\n\n```python\nfrom cnosdb_connector import connect\n\nconn = connect(url="http://127.0.0.1:31007/", user="root", password="")\n\nquery = "insert test_insert(TIME, column1, column2, column3, column4, column5, column6, column7) values (100, -1234, \'hello\', 1234, false, 1.2, \'beijing\', \'shanghai\'); "\n\nconn.execute(query)\n\nresp = conn.execute("SELECT * FROM test_insert;")\nprint(resp)\n```\n\n#### Write use CSV\n\n```python\nfrom cnosdb_connector import connect\nimport os\n\nquery = "CREATE TABLE test_insert(column1 BIGINT CODEC(DELTA),\\\n                                  column2 BOOLEAN,\\\n                                  column3 DOUBLE CODEC(GORILLA),\\\n                                  TAGS(column4));"\n\nconn = connect(url="http://127.0.0.1:31007/", user="root", password="")\n# table schema must same with csv file\nconn.execute(query)\n\npath = os.path.abspath("test.csv")\nconn.write_csv("test_insert", path)\n\nresp = conn.execute("SELECT * FROM test_insert;")\nprint(resp)\n```\n\n# License\n\nCnosDB Python Connector use MIT License',
    'author': 'Subsegment',
    'author_email': '304741833@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
