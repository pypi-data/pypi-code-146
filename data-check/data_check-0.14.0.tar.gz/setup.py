# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['data_check',
 'data_check.checks',
 'data_check.checks.pipeline_check',
 'data_check.cli',
 'data_check.fake',
 'data_check.fake.iterators',
 'data_check.output',
 'data_check.sql',
 'data_check.utils']

package_data = \
{'': ['*']}

install_requires = \
['Faker==16.3.0',
 'Jinja2==3.1.2',
 'SQLAlchemy==1.4.46',
 'click-default-group==1.2.2',
 'click==8.1.3',
 'colorama==0.4.6',
 'numpy==1.24.1',
 'openpyxl==3.0.10',
 'pandas==1.5.2',
 'python-dateutil==2.8.2',
 'pyyaml==6.0']

extras_require = \
{'mssql': ['pyodbc==4.0.35'],
 'mysql': ['pymysql[rsa]==1.0.2'],
 'oracle': ['cx_Oracle==8.3.0'],
 'postgres': ['psycopg2-binary==2.9.5']}

entry_points = \
{'console_scripts': ['data_check = data_check.cli.main:cli']}

setup_kwargs = {
    'name': 'data-check',
    'version': '0.14.0',
    'description': 'simple data validation',
    'long_description': '# data_check\n\ndata_check is a simple data validation tool. In its most basic form it will execute SQL queries and compare the results against CSV or Excel files. But there are more advanced features:\n\n## Features\n\n* [CSV checks](https://andrjas.github.io/data_check/csv_checks/): compare SQL queries against CSV files\n* Excel support: Use Excel (xlsx) instead of CSV\n* multiple environments (databases) in the configuration file\n* [populate tables](https://andrjas.github.io/data_check/loading_data/) from CSV or Excel files\n* [execute any SQL files on a database](https://andrjas.github.io/data_check/sql/)\n* more complex [pipelines](https://andrjas.github.io/data_check/pipelines/)\n* run any script/command (via pipelines)\n* simplified checks for [empty datasets](https://andrjas.github.io/data_check/csv_checks/#empty-dataset-checks) and [full table comparison](https://andrjas.github.io/data_check/csv_checks/#full-table-checks)\n* [lookups](https://andrjas.github.io/data_check/csv_checks/#lookups) to reuse the same data in multiple queries\n* [test data generation](https://andrjas.github.io/data_check/test_data/)\n\n## Database support\n\ndata_check should work with any database that works with [SQLAlchemy](https://docs.sqlalchemy.org/en/14/dialects/). Currently data_check is tested against PostgreSQL, MySQL, SQLite, Oracle and Microsoft SQL Server.\n\n## Quickstart\n\nYou need Python 3.8 or above to run data_check. The easiest way to install data_check is via [pipx](https://github.com/pipxproject/pipx):\n\n`pipx install data-check`\n\nThe data_check Git repository is also a sample data_check project. Clone the repository, switch to the folder and run data_check:\n\n```\ngit clone git@github.com:andrjas/data_check.git\ncd data_check/example\ndata_check\n```\n\nThis will run the tests in the _checks_ folder using the default connection as set in data_check.yml.\n\nSee the [documentation](https://andrjas.github.io/data_check) how to install data_check in different environments with additional database drivers and other usages of data_check.\n\n## Project layout\n\ndata_check has a simple layout for projects: a single configuration file and a folder with the test files. You can also organize the test files in subfolders.\n\n    data_check.yml    # The configuration file\n    checks/           # Default folder for data tests\n        some_test.sql # SQL file with the query to run against the database\n        some_test.csv # CSV file with the expected result\n        subfolder/    # Tests can be nested in subfolders\n\n## CSV checks\n\nThis is the default mode when running data_check. data_check expects a SQL file and a CSV file. The SQL file will be executed against the database and the result is compared with the CSV file. If they match, the test is passed, otherwise it fails.\n\n## Pipelines\n\nIf data_check finds a file named _data\\_check\\_pipeline.yml_ in a folder, it will treat this folder as a pipeline check. Instead of running [CSV checks](#csv-checks) it will execute the steps in the YAML file.\n\nExample project with a pipeline:\n\n    data_check.yml\n    checks/\n        some_test.sql                # this test will run in parallel to the pipeline test\n        some_test.csv\n        sample_pipeline/\n            data_check_pipeline.yml  # configuration for the pipeline\n            data/\n                my_schema.some_table.csv       # data for a table\n            data2/\n                some_data.csv        # other data\n            some_checks/             # folder with CSV checks\n                check1.sql\n                check1.csl\n                ...\n            run_this.sql             # a SQL file that will be executed\n            cleanup.sql\n        other_pipeline/              # you can have multiple pipelines that will run in parallel\n            data_check_pipeline.yml\n            ...\n\nThe file _sample\\_pipeline/data\\_check\\_pipeline.yml_ can look like this:\n\n```yaml\nsteps:\n    # this will truncate the table my_schema.some_table and load it with the data from data/my_schema.some_table.csv\n    - load: data\n    # this will execute the SQL statement in run_this.sql\n    - sql: run_this.sql\n    # this will append the data from data2/some_data.csv to my_schema.other_table\n    - load:\n        file: data2/some_data.csv\n        table: my_schema.other_table\n        mode: append\n    # this will run a python script and pass the connection name\n    - cmd: "python3 /path/to/my_pipeline.py --connection {{CONNECTION}}"\n    # this will run the CSV checks in the some_checks folder\n    - check: some_checks\n```\n\nPipeline checks and simple CSV checks can coexist in a project.\n\n## Documentation\n\nSee the [documentation](https://andrjas.github.io/data_check) how to setup data_check, how to create a new project and more options.\n\n## License\n\n[MIT](LICENSE)\n',
    'author': 'Andreas Rjasanow',
    'author_email': 'andrjas@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://andrjas.github.io/data_check/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
