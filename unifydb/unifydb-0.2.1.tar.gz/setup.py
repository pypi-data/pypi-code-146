# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gsheets_unify_adapter',
 'gsheets_unify_adapter.tests',
 'unify',
 'unify.tests',
 'unify_kernel']

package_data = \
{'': ['*'], 'unify.tests': ['files/*']}

install_requires = \
['altair-viewer>=0.4.0,<0.5.0',
 'altair>=4.2.0,<5.0.0',
 'clickhouse-driver>=0.2.5,<0.3.0',
 'clickhouse-sqlalchemy>=0.2.3,<0.3.0',
 'duckdb-engine>=0.6.8,<0.7.0',
 'duckdb>=0.6.1,<0.7.0',
 'google-api-python-client>=2.70.0,<3.0.0',
 'google-auth-httplib2>=0.1.0,<0.2.0',
 'google-auth-oauthlib>=0.8.0,<0.9.0',
 'ipykernel>=6.19.4,<7.0.0',
 'ipynbname>=2021.3.2,<2022.0.0',
 'jsonpath-ng>=1.5.3,<2.0.0',
 'lark>=1.1.5,<2.0.0',
 'nb2mail-unify>=0.6,<0.7',
 'pandas>=1.5.2,<2.0.0',
 'prompt-toolkit>=3.0.36,<4.0.0',
 'pyaml>=21.10.1,<22.0.0',
 'pyarrow>=10.0.1,<11.0.0',
 'pytest>=7.2.0,<8.0.0',
 'pyzmq>=24.0.1,<25.0.0',
 'readem>=1.0.2,<2.0.0',
 'redmail>=0.4.2,<0.5.0',
 'requests-aws4auth>=1.1.2,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'signaling>=1.0.0,<2.0.0',
 'sqlalchemy>=1.4.45,<2.0.0',
 'sqlglot>=10.3.2,<11.0.0']

setup_kwargs = {
    'name': 'unifydb',
    'version': '0.2.1',
    'description': 'Your personal data warehouse',
    'long_description': '# Unify\n\nUnify is a simple tool which allows you to use SQL to query information from any\ncloud based system that supports a REST API. \n\nSystem APIs are described in a configuration which models API endpoints as tables.\nThe JSON payload results from API calls are automatically flattened so that\nresult fields become columns in the table.\n\nThe tables representing the API endpoints for each system are grouped under a database schema.\n\nAfter data is downloaded via API calls, it is stored to a local database (using DuckDB).\n\n## Example\n\nQuerying the list of repositories you have access to on Github:\n\n    > select id, name, owner_login, open_issues_count from github.repos;\n    id                                  name owner_login  open_issues_count\n    51189180                           philo   tatari-tv                 74\n    51713527                        pytrends   tatari-tv                  0\n    63492894                        philo-fe   tatari-tv                 30\n    67756418                     grey-matter   tatari-tv                 34\n\n## Getting started\n\nCopy [dotenv_template](dotenv_template) to `.env` and edit values to match your environment.\n\nThe easiest way to start is by using DuckDB which provides an embedded database. Just\nset the `DATABASE_BACKEND=duckdb`.\n\nNow run the command interpreter:\n\n    python -m unify\n\nTo add connections to external systems, edit the `unify_connections.yaml` file in your\nhome or current directory. See [connections_example.yaml](connections_example.yaml) for the format.\n\n## Configuration\n\nREST API configurations are defined in YAML and stored in the `rest_specs` folder.\nConsult [spec_doc.yaml](./rest_specs/spec_doc.yaml) for the specification. To\ncreate access to a new system you just need to create a new YAML file describing\nthe system and restart the server.\n\n## Connections\n\n"Connections" define authentication into a particular account of a cloud system.\nYou need to define a connection for each cloud system you want to access. That\nconnection should reference the REST API spec (by name), and provide authentication\ndetails.\n\nThe connections file holds a list of connection definitions, that looks like:\n\n    - <schema name>\n      spec: <REST API spec file prefix>\n      options:\n        <key>: <value>\n        <key>: <value>\n\nThe "spec" field value should match the prefix of one of the "rest_spec" files. That\nfile will usually reference variables in its `auth` block. You should define values\nfor those variables in the `options` section of the connection.\n\nYou can store sensitive values directly into `connections.yml`, or you can use\n`$<name>` syntax to reference an environment variable and store secrets in the\nenvironment instead.\n\n## Variables\n\nUnify extends normal SQL syntax to support `$name` format variables:\n\n    $last_record = <expr>\n    $VAR1 = <expr>\n    \nwhere <expr> will generally be either a scalar expression, including some literal value, or\nthe result of a SELECT query.\n\nExamples:\n\n    $current = select current_date\n    $maxval = 100\n\n    $last_item = select * from items order by created desc limit 1\n\nVariables that use all upper case letters are automatically treated as globals, meaning\nthey are globally defined, available, and persistent. Other variables are considered transient\nand only live the lifetime a session.\n\nCreating a variable as the result of a select statement is equivalent to creating\na _materialized_ view - the query is evaulated immediately and the results are stored\nas the present and future value of the variable. To create a variable which executes the\nquery each time it is used you should just create a normal `view` using `create view`.\n\nNote that variables are automatically persisted across sessions. Use `unset` to\ndelete a variable:\n\n    unset $scotts_items\n\n## Exporting data\n\nSome Adapters can support writing results to their connected system. Generally we don\'t\ntry to follow `create table` semantics as much as "data export" semantics. This implies\nthat data is "exported" to the target system as "append only". Typical use cases\nare exporting data to files on S3 or Google Sheets. \n\nSee the [SQL LANGUAGE](docs/SQL_LANGUAGE.md) docs for syntax.\n\n\n## TODO\n\nSee [TODO](docs/TODO.md)\n\n\n### Adapters\n\n- Implement some interesting new adapters: Gmail, Salesforce, S3, GDrive\n- Implement YAMLSchema validation for adapter specs\n- A Web based "adapter builder" for interactive building/modifying of adapter specs\n- Generalizeed Oauth support\n\n### Interpreter\n\n- Proper command/table/column completion\n\n### Web interface\n\n- Build a centralized web admin front-end for interacting with the interpreter\n- Data exploration interfaces\n    - Create connection interface\n    - Schema browser\n    - Data "peeking" (both tables and API endpoints)\n    - Adapter builder\n    - Command console\n- Proprietary "notebook" support. A notebook is a similar to Jupyter - a sequential set of cells\nwhere cells are either code or right text. Notebooks also include "input" and "output" metadata.\nThat is, notebooks automatically describe which tables/vars they depend on for input, and which ones\nthey generate as output. This allows the user to decompose a complex pipeline into multiple notebooks,\nwhere the system automatically understands the dependencies between the pieces. The user can annotate\na notebook to "auto execute" if any of its inputs change. So if I imported a spreadsheet into a table,\nthen created a notebook to transform the sheet data into another table, then I could specify that\nthe notebook should be executed automatically if the original sheet data was updated.\n- Implement support for "reports" and "dashboards" either as new first-class objects or specializations\nof notebooks. Likely to be the latter. You create a notebook and then say "render this notebook as\na dashboard" which basically extracts and displays only "marked reportable" cells. By default a code\ncell which makes a chart will be marked "reportable". But the user could elect to report via tables or\ntext cells as well.\n- Notebook "dev/publish" mode should be very clear. A notebook can only be run automatically in the background\nonce it is "published" which creates a "hard version" of the notebook contents. This let\'s someone play\nwith notebook edits without affecting published notebooks. (Maybe "published" notebooks are commited into\nthe interpreter, while dev notebooks are only held in the admin layer?)\n\n## Developing\n\nMake sure to setup the environment with:\n\n    export $(cat .env)\n    \n## Metrics use cases\n\n- Quality metrics\n  - Count of P1/P2 incidents by month\n  - Tickets opened vs. closed\n  - Revenue chart\n  - Count of DQ tickets (by tag)\n  - Costs\n    - 30 day lookback for\n      - AWS costs by service\n      - Datadog\n      - Papertrail\n\n## Running Metabase\n\nMetabase supports Clickhouse, so you can run Metabase and connect it directly to the CH db.\nRunning Metabase directly from the jar is easy as long as you get the right (OpenJDK) version.\n\nInstall `clickhouse.metabase-driver.jar` in the plugins directory and that will let you \nadd the Clickhouse connection.\n',
    'author': 'Scott Persinger',
    'author_email': 'scottpersinger@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/scottpersinger/unify',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
