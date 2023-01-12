# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['databudgie', 'databudgie.adapter', 'databudgie.cli', 'databudgie.manifest']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0.0',
 'configly[yaml]',
 'rich',
 'sqlalchemy>=1.3',
 'strapp[click,sqlalchemy]>=0.2.7']

extras_require = \
{':python_version < "3.8"': ['typing-extensions>=3.10.0', 'importlib-metadata'],
 'psycopg2': ['psycopg2>=2.7'],
 'psycopg2-binary': ['psycopg2-binary>=2.7'],
 's3': ['boto3'],
 'sentry': ['sentry-sdk']}

entry_points = \
{'console_scripts': ['databudgie = databudgie.__main__:run']}

setup_kwargs = {
    'name': 'databudgie',
    'version': '2.7.2',
    'description': 'Ergonomic and flexible tool for database backup and restore',
    'long_description': '# Databudgie\n\n![Github Actions Build](https://github.com/schireson/databudgie/actions/workflows/build.yml/badge.svg)\n[![Coverage Status](https://coveralls.io/repos/github/schireson/databudgie/badge.svg?branch=main&t=6I0aU6)](https://coveralls.io/github/schireson/databudgie?branch=main)\n[![Documentation\nStatus](https://readthedocs.org/projects/databudgie/badge/?version=latest)](https://databudgie.readthedocs.io)\n\n![](docs/source/_static/databudgie.png)\n\nDatabudgie is a CLI & library for database performing targeted backup and restore\nof database tables or arbitrary queries against database tables.\n\n# Usage\n\nA minimal config file might look like:\n\n```yaml\n# config.databudgie.yml\nbackup:\n  url: postgresql://postgres:postgres@localhost:5432/postgres\n  tables:\n    - name: public.product\n      query: "select * from {table} where store_id > 4"\n      location: s3://my-s3-bucket/databudgie/public.product\nrestore:\n  url: postgresql://postgres:postgres@localhost:5432/postgres\n  tables:\n    - name: public.product\n      location: s3://my-s3-bucket/databudgie/public.product\n```\n\nWith that config in place, backing up the defined tables (using the specified config)\nis as simple as `databudgie backup`; and restore `databudgie restore`.\n\n## Installation\n\n```bash\npip install databudgie\n```\n',
    'author': 'Andrew Sosa',
    'author_email': 'andrewso@known.is',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/schireson/databudgie',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
