# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sql_cli',
 'sql_cli.astro',
 'sql_cli.cli',
 'sql_cli.operators',
 'sql_cli.utils']

package_data = \
{'': ['*'],
 'sql_cli': ['include/base/*',
             'include/base/.airflow/dags/*',
             'include/base/.airflow/dags/include/*',
             'include/base/.airflow/default/*',
             'include/base/.airflow/dev/*',
             'include/base/config/*',
             'include/base/config/default/*',
             'include/base/config/dev/*',
             'include/base/data/*',
             'include/base/workflows/example_basic_transform/*',
             'include/base/workflows/example_load_file/*',
             'include/base/workflows/example_templating/*',
             'macros/*',
             'templates/*']}

install_requires = \
['Jinja2>=2.10.1,<=3.1',
 'PyYAML>=5.4.1',
 'apache-airflow>2.1',
 'astro-sdk-python[all]>=1.2.2,<2.0.0',
 'black',
 'python-dotenv>=0.21.0,<0.22.0',
 'python-frontmatter>=1.0.0,<2.0.0',
 'typer[all]>=0.6.1,<0.7.0']

extras_require = \
{':python_version < "3.8"': ['networkx>=2.6.3,<3.0.0'],
 ':python_version >= "3.8"': ['networkx>=2.8.7,<3.0.0']}

entry_points = \
{'console_scripts': ['flow = sql_cli.__main__:app']}

setup_kwargs = {
    'name': 'astro-sql-cli',
    'version': '0.3.0a3',
    'description': 'Empower analysts to build workflows to transform data using SQL',
    'long_description': '# Astro SQL CLI\n\nEmpower analysts to build workflows to transform data using SQL.\n\nFind out more in the [docs](https://docs.astronomer.io/astro/cli/sql-cli).\n\n## Getting started\n\n### Install\n\n```bash\n    pip install astro-sql-cli\n```\n\n### Try it out\n\n```bash\n    flow version\n```\n\n\n## Development\n\nSetup your local environment:\n\n```bash\n    make setup\n```\n\nTry your own version of the SQL CLI locally:\n\n```bash\n    poetry run flow version\n```\n\nRun the tests:\n\n```bash\n    make test\n```\n',
    'author': 'Astronomer',
    'author_email': 'humans@astronomer.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
