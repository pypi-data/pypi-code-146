# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['databricks',
 'databricks.sql',
 'databricks.sql.auth',
 'databricks.sql.experimental',
 'databricks.sql.thrift_api',
 'databricks.sql.thrift_api.TCLIService']

package_data = \
{'': ['*']}

install_requires = \
['lz4>=4.0.2,<5.0.0',
 'oauthlib>=3.1.0,<4.0.0',
 'pandas>=1.3.0,<2.0.0',
 'requests>=2.18.1,<3.0.0',
 'thrift>=0.16.0,<0.17.0']

extras_require = \
{':python_version >= "3.11"': ['pyarrow>=10.0.1'],
 ':python_version >= "3.7" and python_version < "3.11"': ['pyarrow>=9.0.0'],
 ':python_version >= "3.7" and python_version < "3.8"': ['numpy==1.21.1'],
 ':python_version >= "3.8"': ['numpy==1.23.4']}

setup_kwargs = {
    'name': 'databricks-sql-connector',
    'version': '2.3.0',
    'description': 'Databricks SQL Connector for Python',
    'long_description': "# Databricks SQL Connector for Python\n\n[![PyPI](https://img.shields.io/pypi/v/databricks-sql-connector?style=flat-square)](https://pypi.org/project/databricks-sql-connector/)\n[![Downloads](https://pepy.tech/badge/databricks-sql-connector)](https://pepy.tech/project/databricks-sql-connector)\n\nThe Databricks SQL Connector for Python allows you to develop Python applications that connect to Databricks clusters and SQL warehouses. It is a Thrift-based client with no dependencies on ODBC or JDBC. It conforms to the [Python DB API 2.0 specification](https://www.python.org/dev/peps/pep-0249/).\n\nThis connector uses Arrow as the data-exchange format, and supports APIs to directly fetch Arrow tables. Arrow tables are wrapped in the `ArrowQueue` class to provide a natural API to get several rows at a time.\n\nYou are welcome to file an issue here for general use cases. You can also contact Databricks Support [here](help.databricks.com).\n\n## Requirements\n\nPython 3.7 or above is required.\n\n## Documentation\n\nFor the latest documentation, see\n\n- [Databricks](https://docs.databricks.com/dev-tools/python-sql-connector.html)\n- [Azure Databricks](https://docs.microsoft.com/en-us/azure/databricks/dev-tools/python-sql-connector)\n\n## Quickstart\n\nInstall the library with `pip install databricks-sql-connector`\n\nExample usage:\n\n```python\nfrom databricks import sql\n\nconnection = sql.connect(\n  server_hostname='********.databricks.com',\n  http_path='/sql/1.0/endpoints/****************',\n  access_token='dapi********************************')\n\n\ncursor = connection.cursor()\n\ncursor.execute('SELECT * FROM RANGE(10)')\nresult = cursor.fetchall()\nfor row in result:\n  print(row)\n\ncursor.close()\nconnection.close()\n```\n\nIn the above example:\n- `server-hostname` is the Databricks instance host name.\n- `http-path` is the HTTP Path either to a Databricks SQL endpoint (e.g. /sql/1.0/endpoints/1234567890abcdef),\nor to a Databricks Runtime interactive cluster (e.g. /sql/protocolv1/o/1234567890123456/1234-123456-slid123)\n- `personal-access-token` is the Databricks Personal Access Token for the account that will execute commands and queries\n\n\n## Contributing\n\nSee [CONTRIBUTING.md](CONTRIBUTING.md)\n\n## License\n\n[Apache License 2.0](LICENSE)\n",
    'author': 'Databricks',
    'author_email': 'databricks-sql-connector-maintainers@databricks.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
