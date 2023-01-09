# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['udata_hydra', 'udata_hydra.utils']

package_data = \
{'': ['*'], 'udata_hydra': ['migrations/*']}

install_requires = \
['aiocontextvars>=0.2.2,<0.3.0',
 'aiohttp>=3.8.1,<4.0.0',
 'asyncpg-trek>=0.2.1,<0.3.0',
 'asyncpg>=0.27.0,<0.28.0',
 'boto3>=1.21.21,<2.0.0',
 'cchardet>=2.1.7,<3.0.0',
 'coloredlogs>=15.0.1,<16.0.0',
 'humanfriendly>=10.0,<11.0',
 'marshmallow>=3.14.1,<4.0.0',
 'minicli>=0.5.0,<0.6.0',
 'pandas>=1.3.3,<2.0.0',
 'progressist>=0.1.0,<0.2.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'python-dotenv>=0.19.2,<0.20.0',
 'python-magic>=0.4.25,<0.5.0',
 'redis>=4.1.4,<5.0.0',
 'rq>=1.11.1,<2.0.0',
 'sentry-sdk>=1.11.1,<2.0.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['udata-hydra = udata_hydra.cli:run',
                     'udata-hydra-app = udata_hydra.app:run',
                     'udata-hydra-crawl = udata_hydra.crawl:run']}

setup_kwargs = {
    'name': 'udata-hydra',
    'version': '1.0.2.dev748',
    'description': 'Async crawler and datalake service for data.gouv.fr',
    'long_description': '# udata-hydra 🦀\n\n`udata-hydra` is an async metadata crawler for [data.gouv.fr](https://www.data.gouv.fr).\n\nURLs are crawled via _aiohttp_, catalog and crawled metadata are stored in a _PostgreSQL_ database.\n\n## CLI\n\n### Create database structure\n\nInstall udata-hydra dependencies and cli.\n`poetry install`\n\n`poetry run udata-hydra migrate`\n\n### Load (UPSERT) latest catalog version from data.gouv.fr\n\n`udata-hydra load-catalog`\n\n## Crawler\n\n`udata-hydra-crawl`\n\nIt will crawl (forever) the catalog according to config set in `config.py`.\n\n`BATCH_SIZE` URLs are queued at each loop run.\n\nThe crawler will start with URLs never checked and then proceed with URLs crawled before `SINCE` interval. It will then wait until something changes (catalog or time).\n\nThere\'s a by-domain backoff mecanism. The crawler will wait when, for a given domain in a given batch, `BACKOFF_NB_REQ` is exceeded in a period of `BACKOFF_PERIOD` seconds. It will retry until the backoff is lifted.\n\nIf an URL matches one of the `EXCLUDED_PATTERNS`, it will never be checked.\n\n## Worker\n\nA job queuing system is used to process long-running tasks. Launch the worker with the following command:\n\n`poetry run rq worker -c udata_hydra.worker`\n\n## API\n\n### Run\n\n```\npoetry install\npoetry run adev runserver udata_hydra/app.py\n```\n\n### Get latest check\n\nWorks with `?url={url}` and `?resource_id={resource_id}`.\n\n```\n$ curl -s "http://localhost:8000/api/checks/latest/?url=http://opendata-sig.saintdenis.re/datasets/661e19974bcc48849bbff7c9637c5c28_1.csv" | json_pp\n{\n   "status" : 200,\n   "catalog_id" : 64148,\n   "deleted" : false,\n   "error" : null,\n   "created_at" : "2021-02-06T12:19:08.203055",\n   "response_time" : 0.830198049545288,\n   "url" : "http://opendata-sig.saintdenis.re/datasets/661e19974bcc48849bbff7c9637c5c28_1.csv",\n   "domain" : "opendata-sig.saintdenis.re",\n   "timeout" : false,\n   "id" : 114750,\n   "dataset_id" : "5c34944606e3e73d4a551889",\n   "resource_id" : "b3678c59-5b35-43ad-9379-fce29e5b56fe",\n   "headers" : {\n      "content-disposition" : "attachment; filename=\\"xn--Dlimitation_des_cantons-bcc.csv\\"",\n      "server" : "openresty",\n      "x-amz-meta-cachetime" : "191",\n      "last-modified" : "Wed, 29 Apr 2020 02:19:04 GMT",\n      "content-encoding" : "gzip",\n      "content-type" : "text/csv",\n      "cache-control" : "must-revalidate",\n      "etag" : "\\"20415964703d9ccc4815d7126aa3a6d8\\"",\n      "content-length" : "207",\n      "date" : "Sat, 06 Feb 2021 12:19:08 GMT",\n      "x-amz-meta-contentlastmodified" : "2018-11-19T09:38:28.490Z",\n      "connection" : "keep-alive",\n      "vary" : "Accept-Encoding"\n   }\n}\n```\n\n### Get all checks for an URL or resource\n\nWorks with `?url={url}` and `?resource_id={resource_id}`.\n\n```\n$ curl -s "http://localhost:8000/api/checks/all/?url=http://www.drees.sante.gouv.fr/IMG/xls/er864.xls" | json_pp\n[\n   {\n      "domain" : "www.drees.sante.gouv.fr",\n      "dataset_id" : "53d6eadba3a72954d9dd62f5",\n      "timeout" : false,\n      "deleted" : false,\n      "response_time" : null,\n      "error" : "Cannot connect to host www.drees.sante.gouv.fr:443 ssl:True [SSLCertVerificationError: (1, \\"[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: Hostname mismatch, certificate is not valid for \'www.drees.sante.gouv.fr\'. (_ssl.c:1122)\\")]",\n      "catalog_id" : 232112,\n      "url" : "http://www.drees.sante.gouv.fr/IMG/xls/er864.xls",\n      "headers" : {},\n      "id" : 165107,\n      "created_at" : "2021-02-06T14:32:47.675854",\n      "resource_id" : "93dfd449-9d26-4bb0-a6a9-ee49b1b8a4d7",\n      "status" : null\n   },\n   {\n      "timeout" : false,\n      "deleted" : false,\n      "response_time" : null,\n      "error" : "Cannot connect to host www.drees.sante.gouv.fr:443 ssl:True [SSLCertVerificationError: (1, \\"[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: Hostname mismatch, certificate is not valid for \'www.drees.sante.gouv.fr\'. (_ssl.c:1122)\\")]",\n      "domain" : "www.drees.sante.gouv.fr",\n      "dataset_id" : "53d6eadba3a72954d9dd62f5",\n      "created_at" : "2020-12-24T17:06:58.158125",\n      "resource_id" : "93dfd449-9d26-4bb0-a6a9-ee49b1b8a4d7",\n      "status" : null,\n      "catalog_id" : 232112,\n      "url" : "http://www.drees.sante.gouv.fr/IMG/xls/er864.xls",\n      "headers" : {},\n      "id" : 65092\n   }\n]\n```\n\n### Get crawling status\n\n```\n$ curl -s "http://localhost:8000/api/status/crawler/" | json_pp\n{\n   "fresh_checks_percentage" : 0.4,\n   "pending_checks" : 142153,\n   "total" : 142687,\n   "fresh_checks" : 534,\n   "checks_percentage" : 0.4\n}\n```\n\n### Get worker status\n\n```\n$ curl -s "http://localhost:8000/api/status/worker/" | json_pp\n{\n   "queued" : {\n      "default" : 0,\n      "high" : 825,\n      "low" : 655\n   }\n}\n```\n\n### Get crawling stats\n\n```\n$ curl -s "http://localhost:8000/api/stats/" | json_pp\n{\n   "status" : [\n      {\n         "count" : 525,\n         "percentage" : 98.3,\n         "label" : "ok"\n      },\n      {\n         "label" : "error",\n         "percentage" : 1.3,\n         "count" : 7\n      },\n      {\n         "label" : "timeout",\n         "percentage" : 0.4,\n         "count" : 2\n      }\n   ],\n   "status_codes" : [\n      {\n         "code" : 200,\n         "count" : 413,\n         "percentage" : 78.7\n      },\n      {\n         "code" : 501,\n         "percentage" : 12.4,\n         "count" : 65\n      },\n      {\n         "percentage" : 6.1,\n         "count" : 32,\n         "code" : 404\n      },\n      {\n         "code" : 500,\n         "percentage" : 2.7,\n         "count" : 14\n      },\n      {\n         "code" : 502,\n         "count" : 1,\n         "percentage" : 0.2\n      }\n   ]\n}\n```\n\n## Using Webhook integration\n\n** Set the config values**\n\nCreate a `config.toml` where your service and commands are launched, or specify a path to a TOML file via the `HYDRA_SETTINGS` environment variable. `config.toml` or equivalent will override values from `udata_hydra/config_default.toml`, lookup there for values that can/need to be defined.\n\n```toml\nUDATA_URI = "https://dev.local:7000/api/2"\nUDATA_URI_API_KEY = "example.api.key"\nSENTRY_DSN = "https://{my-sentry-dsn}"\n```\n\nThe webhook integration sends HTTP messages to `udata` when resources are analyzed or checked to fill resources extras.\n\nRegarding analysis, there is a phase called "change detection". It will try to guess if a resource has been modified based on different criterions:\n- harvest modified date in catalog\n- content-length and last-modified headers\n- checksum comparison over time\n\nThe payload should look something like:\n\n```json\n{\n   "analysis:filesize": 91661,\n   "analysis:mime-type": "application/zip",\n   "analysis:checksum": "bef1de04601dedaf2d127418759b16915ba083be",\n   "analysis:last-modified-at": "2022-11-27T23:00:54.762000",\n   "analysis:last-modified-detection": "harvest-resource-metadata",\n}\n```\n\n## Development\n\n### docker-compose\n\nMultiple docker-compose files are provided:\n- a minimal `docker-compose.yml` with PostgreSQL\n- `docker-compose.broker.yml` adds a Redis broker\n- `docker-compose.test.yml` launches a test DB, needed to run tests\n\nNB: you can launch compose from multiple files like this: `docker-compose -f docker-compose.yml -f docker-compose.test.yml up`\n\n### Logging & Debugging\n\nThe log level can be adjusted using the environment variable LOG_LEVEL.\nFor example, to set the log level to `DEBUG` when initializing the database, use `LOG_LEVEL="DEBUG" udata-hydra init_db `.\n\n### Writing a migration\n\n1. Add a file named `migrations/{YYYYMMDD}_{from}_up_{to}.sql` and write the SQL you need to perform migration. `from` should be the revision from before (eg `rev1`), `to` the revision you\'re aiming at (eg `rev2`)\n2. Modify the latest revision (eg `rev2`) in `migrations/_LATEST_REVISION`\n3. `udata-hydra migrate` will use the info from `_LATEST_REVISION` to upgrade to `rev2`. You can also specify `udata-hydra migrate --revision rev2`\n\n## Deployment\n\n3 services need to be deployed for the full stack to run:\n- worker\n- api / app\n- crawler\n\nRefer to each section to learn how to launch them. The only differences from dev to prod are:\n- use `HYDRA_SETTINGS` env var to point to your custom `config.toml`\n- use `HYDRA_APP_SOCKET_PATH` to configure where aiohttp should listen to a [reverse proxy connection (eg nginx)](https://docs.aiohttp.org/en/stable/deployment.html#nginx-configuration) and use `udata-hydra-app` to launch the app server\n',
    'author': 'Opendata Team',
    'author_email': 'opendatateam@data.gouv.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
