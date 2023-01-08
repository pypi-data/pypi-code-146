# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tracktolib', 'tracktolib.pg', 'tracktolib.s3']

package_data = \
{'': ['*']}

extras_require = \
{'api': ['fastapi>=0.88.0,<0.89.0'],
 'http': ['httpx>=0.23.0,<0.24.0'],
 'logs': ['python-json-logger>=2.0.4,<3.0.0'],
 'pg': ['asyncpg>=0.27.0,<0.28.0', 'rich>=12.6.0,<13.0.0'],
 'pg-sync': ['psycopg>=3.1.5,<4.0.0'],
 's3': ['aiobotocore>=2.4.0,<3.0.0'],
 's3-minio': ['minio>=7.1.13,<8.0.0'],
 'tests': ['deepdiff>=6.2.1,<7.0.0']}

setup_kwargs = {
    'name': 'tracktolib',
    'version': '0.21.1',
    'description': 'Utility library for python',
    'long_description': "# Tracktolib\n\n[![Python versions](https://img.shields.io/pypi/pyversions/tracktolib)](https://pypi.python.org/pypi/tracktolib)\n[![Latest PyPI version](https://img.shields.io/pypi/v/tracktolib?logo=pypi)](https://pypi.python.org/pypi/tracktolib)\n[![CircleCI](https://circleci.com/gh/Tracktor/tracktolib/tree/master.svg?style=shield)](https://app.circleci.com/pipelines/github/Tracktor/tracktolib?branch=master)\n\nUtility library for python\n\n# Installation\n\nYou can choose to not install all the dependencies by specifying\nthe [extra](https://python-poetry.org/docs/cli/#options-4) parameter such as:\n\n```bash\npoetry add tracktolib@latest -E pg-sync -E tests --group dev \n```\n\nHere we only install the utilities using `psycopg` (pg-sync) and `deepdiff` (tests) for the dev environment.\n\n# Utilities\n\n- **log**\n\nUtility functions for logging.\n\n```python\nimport logging\nfrom tracktolib.logs import init_logging\n\nlogger = logging.getLogger()\nformatter, stream_handler = init_logging(logger, 'json', version='0.0.1')\n```\n\n- **pg**  \n\nUtility functions for [asyncpg](https://github.com/MagicStack/asyncpg)\n\n- **pg-sync**\n\nUtility functions based on psycopg such as `fetch_one`, `insert_many`, `fetch_count` ...\n\nTo use the functions, create a `Connection` using psycopg: `conn = psycopg2.connect()`\n\n*fetch_one*\n\n```python\nfrom pg.pg_sync import (\n    insert_many, fetch_one, fetch_count, fetch_all\n)\n\ndata = [\n    {'foo': 'bar', 'value': 1},\n    {'foo': 'baz', 'value': 2}\n]\ninsert_many(conn, 'public.test', data)  # Will insert the 2 dict\nquery = 'SELECT foo from public.test order by value asc'\nvalue = fetch_one(conn, query, required=True)  # Will return {'foo': 'bar'}, raise an error is not found\nassert fetch_count(conn, 'public.test') == 2\nquery = 'SELECT * from public.test order by value asc'\nassert fetch_all(conn, query) == data\n\n```\n\n- **tests**\n\nUtility functions for tests such as `get_uuid` (that generates a test uuid based on an integer)\n\n*get_uuid*\n\n```python\nfrom tracktolib.tests import get_uuid\n\nassert get_uuid(1) == '00000000-0000-0000-0000-000000000001'\n```\n\n- **s3-minio**\n\nUtility functions for [minio](https://min.io/docs/minio/linux/developers/python/API.html)\n\n- **s3**\n\nUtility functions for [aiobotocore](https://github.com/aio-libs/aiobotocore)\n\n- **logs**\n\nUtility functions to initialize the logging formatting and streams\n\n- **http**\n\nUtility functions using [httpx](https://www.python-httpx.org/)\n\n- **api**\n\nUtility functions using [fastapi](https://fastapi.tiangolo.com/)\n",
    'author': 'Julien Brayere',
    'author_email': 'julien.brayere@tracktor.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tracktor/tracktolib',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
