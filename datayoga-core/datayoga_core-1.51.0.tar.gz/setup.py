# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['datayoga_core',
 'datayoga_core.blocks',
 'datayoga_core.blocks.add_field',
 'datayoga_core.blocks.add_field.tests',
 'datayoga_core.blocks.cassandra',
 'datayoga_core.blocks.cassandra.write',
 'datayoga_core.blocks.files.read_csv',
 'datayoga_core.blocks.filter',
 'datayoga_core.blocks.filter.tests',
 'datayoga_core.blocks.map',
 'datayoga_core.blocks.map.tests',
 'datayoga_core.blocks.redis',
 'datayoga_core.blocks.redis.read_stream',
 'datayoga_core.blocks.redis.write',
 'datayoga_core.blocks.relational',
 'datayoga_core.blocks.relational.read',
 'datayoga_core.blocks.relational.write',
 'datayoga_core.blocks.remove_field',
 'datayoga_core.blocks.remove_field.tests',
 'datayoga_core.blocks.rename_field',
 'datayoga_core.blocks.rename_field.tests',
 'datayoga_core.blocks.sequence',
 'datayoga_core.blocks.std',
 'datayoga_core.blocks.std.read',
 'datayoga_core.blocks.std.write']

package_data = \
{'': ['*'],
 'datayoga_core': ['resources/scaffold/*',
                   'resources/scaffold/data/*',
                   'resources/scaffold/jobs/sample/*',
                   'resources/schemas/*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'certifi>=2022.12.7,<2023.0.0',
 'cryptography>=38.0.4,<39.0.0',
 'jmespath>=1.0.0,<2.0.0',
 'jsonschema>=4.4.0,<5.0.0',
 'sqlglot>=11.51.0,<12.0.0']

extras_require = \
{':sys_platform == "linux"': ['pysqlite3-binary>=0.4.0,<0.5.0'],
 'cassandra': ['cassandra-driver>=3.25.0,<4.0.0'],
 'mssql': ['pymssql>=2.2.7,<3.0.0', 'SQLAlchemy>=1.4.44,<2.0.0'],
 'mysql': ['PyMySQL>=1.0.2,<2.0.0', 'SQLAlchemy>=1.4.44,<2.0.0'],
 'pg': ['psycopg2-binary>=2.9.5,<3.0.0', 'SQLAlchemy>=1.4.44,<2.0.0'],
 'redis': ['redis>=4.3.5,<5.0.0'],
 'test': ['mock>=4.0.3,<5.0.0',
          'pytest>=7.1.2,<8.0.0',
          'pytest-asyncio>=0.20.2,<0.21.0',
          'pytest-describe>=2.0.1,<3.0.0',
          'pytest-mock>=3.7.0,<4.0.0',
          'pytest-timeout>=2.1.0,<3.0.0',
          'requests-mock>=1.9.3,<2.0.0',
          'testcontainers>=3.7.0,<4.0.0',
          'cassandra-driver>=3.25.0,<4.0.0',
          'psycopg2-binary>=2.9.5,<3.0.0',
          'pymssql>=2.2.7,<3.0.0',
          'PyMySQL>=1.0.2,<2.0.0',
          'redis>=4.3.5,<5.0.0',
          'SQLAlchemy>=1.4.44,<2.0.0']}

setup_kwargs = {
    'name': 'datayoga-core',
    'version': '1.51.0',
    'description': 'DataYoga for Python',
    'long_description': '# DataYoga Core\n\n## Introduction\n\n`datayoga-core` is the transformation engine used in `DataYoga`, a framework for building and generating data pipelines.\n\n## Installation\n\n```bash\npip install datayoga-core\n```\n\n## Quick Start\n\nThis demonstrates how to transform data using a DataYoga job.\n\n### Create a Job\n\nUse this `example.yaml`:\n\n```yaml\n- steps:\n    - uses: add_field\n      with:\n        fields:\n          - field: full_name\n            language: jmespath\n            expression: concat([fname, \' \' , lname])\n          - field: country\n            language: sql\n            expression: country_code || \' - \' || UPPER(country_name)\n    - uses: rename_field\n      with:\n        fields:\n          - from_field: fname\n            to_field: first_name\n          - from_field: lname\n            to_field: last_name\n    - uses: remove_field\n      with:\n        fields:\n          - field: credit_card\n          - field: country_name\n          - field: country_code\n    - uses: map\n      with:\n        expression:\n          {\n            first_name: first_name,\n            last_name: last_name,\n            greeting: "\'Hello \' || CASE WHEN gender = \'F\' THEN \'Ms.\' WHEN gender = \'M\' THEN \'Mr.\' ELSE \'N/A\' END || \' \' || full_name",\n            country: country,\n            full_name: full_name\n          }\n        language: sql\n```\n\n### Transform Data Using `datayoga-core`\n\nUse this code snippet to transform a data record using the job defined [above](#create-a-job):\n\n```python\nimport datayoga_core as dy\nfrom datayoga_core.job import Job\nfrom datayoga_core.utils import read_yaml\n\njob_settings = read_yaml("example.yaml")\njob = dy.compile(job_settings)\n\nassert job.transform({"fname": "jane", "lname": "smith", "country_code": 1, "country_name": "usa", "credit_card": "1234-5678-0000-9999", "gender": "F"}) == {"first_name": "jane", "last_name": "smith", "country": "1 - USA", "full_name": "jane smith", "greeting": "Hello Ms. jane smith"}\n```\n\nAs can be seen, the record has been transformed based on the job:\n\n- `fname` field renamed to `first_name`.\n- `lname` field renamed to `last_name`.\n- `country` field added based on an SQL expression.\n- `full_name` field added based on a [JMESPath](https://jmespath.org/) expression.\n- `greeting` field added based on an SQL expression.\n\n### Examples\n\n- Add a new field `country` out of an SQL expression that concatenates `country_code` and `country_name` fields after upper case the later:\n\n  ```yaml\n  uses: add_field\n  with:\n    field: country\n    language: sql\n    expression: country_code || \' - \' || UPPER(country_name)\n  ```\n\n- Rename `fname` field to `first_name` and `lname` field to `last_name`:\n\n  ```yaml\n  uses: rename_field\n  with:\n    fields:\n      - from_field: fname\n        to_field: first_name\n      - from_field: lname\n        to_field: last_name\n  ```\n\n- Remove `credit_card` field:\n\n  ```yaml\n  uses: remove_field\n  with:\n    field: credit_card\n  ```\n\nFor a full list of supported block types [see reference](https://datayoga-io.github.io/library).\n\n## Expression Language\n\nDataYoga supports both SQL and [JMESPath](https://jmespath.org/) expressions. JMESPath are especially useful to handle nested JSON data, while SQL is more suited to flat row-like structures.\n\nFor more information about custom functions and supported expression language syntax [see reference](https://datayoga-io.github.io/expressions).\n',
    'author': 'DataYoga',
    'author_email': 'admin@datayoga.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
