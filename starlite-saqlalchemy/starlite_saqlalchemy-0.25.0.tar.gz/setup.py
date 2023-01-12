# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['starlite_saqlalchemy',
 'starlite_saqlalchemy.db',
 'starlite_saqlalchemy.dto',
 'starlite_saqlalchemy.log',
 'starlite_saqlalchemy.repository']

package_data = \
{'': ['*'], 'starlite_saqlalchemy': ['static/*']}

install_requires = \
['asyncpg',
 'hiredis',
 'httpx',
 'msgspec',
 'pydantic',
 'python-dotenv',
 'redis',
 'saq>=0.9.1,<0.10.0',
 'sentry-sdk',
 'sqlalchemy==2.0.0b4',
 'starlite>=1.40.1,<2.0.0',
 'structlog>=22.2.0',
 'tenacity',
 'uvicorn',
 'uvloop']

setup_kwargs = {
    'name': 'starlite-saqlalchemy',
    'version': '0.25.0',
    'description': 'Starlite config plugin with SAQ and SQLAlchemy boilerplate',
    'long_description': '<h1 align="center">starlite-saqlalchemy</h1>\n<p align="center">\n  <img src="https://www.topsport.com.au/assets/images/logo_pulse.svg" width="200" alt="TopSport Pulse"/>\n</p>\n\n<p align="center">\n  <a href="https://pypi.org/project/starlite-saqlalchemy">\n    <img src="https://img.shields.io/pypi/v/starlite-saqlalchemy" alt="PYPI: starlite-saqlalchemy"/>\n  </a>\n  <a href="https://github.com/topsport-com-au/starlite-saqlalchemy/blob/main/LICENSE">\n    <img src="https://img.shields.io/pypi/l/starlite-saqlalchemy?color=blue" alt="License: MIT"/>\n  </a>\n  <a href="https://python.org">\n    <img src="https://img.shields.io/pypi/pyversions/starlite-saqlalchemy" alt="Python: supported versions"/>\n  </a>\n  <a href="https://results.pre-commit.ci/latest/github/topsport-com-au/starlite-saqlalchemy/main">\n    <img alt="pre-commit.ci status" src="https://results.pre-commit.ci/badge/github/topsport-com-au/starlite-saqlalchemy/main.svg"/>\n  </a>\n  <a href="https://bestpractices.coreinfrastructure.org/projects/6646">\n    <img alt="OpenSSF Best Practices" src="https://bestpractices.coreinfrastructure.org/projects/6646/badge">\n  </a>\n  <a href="https://github.com/topsport-com-au/starlite-saqlalchemy/actions/workflows/ci.yml">\n    <img alt="Actions: CI" src="https://github.com/topsport-com-au/starlite-saqlalchemy/actions/workflows/ci.yml/badge.svg?branch=main&event=push"/>\n  </a>\n</p>\n<p align="center">\n  <a href="https://sonarcloud.io/summary/new_code?id=topsport-com-au_starlite-saqlalchemy">\n    <img alt="Reliability Rating" src="https://sonarcloud.io/api/project_badges/measure?project=topsport-com-au_starlite-saqlalchemy&metric=reliability_rating"/>\n  </a>\n  <a href="https://sonarcloud.io/summary/new_code?id=topsport-com-au_starlite-saqlalchemy">\n    <img alt="Quality Gate Status" src="https://sonarcloud.io/api/project_badges/measure?project=topsport-com-au_starlite-saqlalchemy&metric=alert_status"/>\n  </a>\n  <a href="https://sonarcloud.io/summary/new_code?id=topsport-com-au_starlite-saqlalchemy">\n    <img alt="Quality Gate Status" src="https://sonarcloud.io/api/project_badges/measure?project=topsport-com-au_starlite-saqlalchemy&metric=coverage"/>\n  </a>\n  <a href="https://sonarcloud.io/summary/new_code?id=topsport-com-au_starlite-saqlalchemy">\n    <img alt="Quality Gate Status" src="https://sonarcloud.io/api/project_badges/measure?project=topsport-com-au_starlite-saqlalchemy&metric=sqale_rating"/>\n  </a>\n  <a href="https://sonarcloud.io/summary/new_code?id=topsport-com-au_starlite-saqlalchemy">\n    <img alt="Quality Gate Status" src="https://sonarcloud.io/api/project_badges/measure?project=topsport-com-au_starlite-saqlalchemy&metric=security_rating"/>\n  </a>\n  <a href="https://sonarcloud.io/summary/new_code?id=topsport-com-au_starlite-saqlalchemy">\n    <img alt="Quality Gate Status" src="https://sonarcloud.io/api/project_badges/measure?project=topsport-com-au_starlite-saqlalchemy&metric=bugs"/>\n  </a>\n  <a href="https://sonarcloud.io/summary/new_code?id=topsport-com-au_starlite-saqlalchemy">\n    <img alt="Quality Gate Status" src="https://sonarcloud.io/api/project_badges/measure?project=topsport-com-au_starlite-saqlalchemy&metric=vulnerabilities"/>\n  </a>\n</p>\n\nConfiguration for a [Starlite](https://github.com/starlite-api/starlite) application that features:\n\n- SQLAlchemy 2.0\n- SAQ async worker\n- Lots of features!\n\n## Example\n\n```python\nfrom starlite import Starlite, get\n\nfrom starlite_saqlalchemy import ConfigureApp\n\n\n@get("/example")\ndef example_handler() -> dict:\n    """Hello, world!"""\n    return {"hello": "world"}\n\n\napp = Starlite(route_handlers=[example_handler], on_app_init=[ConfigureApp()])\n```\n\n## Features\n\nThe application configured in the above example includes the following configuration.\n\n### Logging after exception handler\n\nReceives and logs any unhandled exceptions raised out of route handling.\n\n### Redis cache\n\nIntegrates a Redis cache backend with Starlite first-class cache support.\n\n### Collection route filters\n\nSupport filtering collection routes by created and updated timestamps, list of ids, and limit/offset\npagination.\n\nIncludes an aggregate `filters` dependency to easily inject all filters into a route handler, e.g,:\n\n```python\nfrom starlite import get\nfrom starlite_saqlalchemy.dependencies import FilterTypes\n\n\n@get()\nasync def get_collection(filters: list[FilterTypes]) -> list[...]:\n    ...\n```\n\n### Gzip compression\n\nConfigures Starlite\'s built-in Gzip compression support.\n\n### Exception handlers\n\nException handlers that translate non-Starlite repository and service object exception\ntypes into Starlite\'s HTTP exceptions.\n\n### Health check\n\nA health check route handler that returns some basic application info.\n\n### Logging\n\nConfigures logging for the application including:\n\n- Queue listener handler, appropriate for asyncio applications\n- Health check route filter so that health check requests don\'t clog your logs\n- An informative log format\n- Configuration for dependency logs\n\n### Openapi config\n\nConfigures OpenAPI docs for the application, including config by environment to allow for easy\npersonalization per application.\n\n### Starlite Response class\n\nA response class that can handle serialization of SQLAlchemy/Postgres UUID types.\n\n### Sentry configuration\n\nJust supply the DSN via environment, and Sentry is configured for you.\n\n### SQLAlchemy\n\nEngine, logging, pooling etc all configurable via environment. We configure starlite and include a\ncustom `before_send` wrapper that inspects the outgoing status code to determine whether the\ntransaction that represents the request should be committed, or rolled back.\n\n### Async SAQ worker config\n\nA customized SAQ queue and worker that is started and shutdown using the Starlite lifecycle event\nhooks - no need to run your worker in another process, we attach it to the same event loop as the\nStarlite app uses. Be careful not to do things in workers that will block the loop!\n\n## Extra Features\n\nIn addition to application config, the library include:\n\n### Repository\n\nAn abstract repository object type and a SQLAlchemy repository implementation.\n\n### DTO Factory\n\nA factory for building pydantic models from SQLAlchemy 2.0 style declarative classes. Use these to\nannotate the `data` parameter and return type of routes to control the data that can be modified per\nroute, and the information included in route responses.\n\n### HTTP Client and Endpoint decorator\n\n`http.Client` is a wrapper around `httpx.AsyncClient` with some extra features including unwrapping\nenveloped data, and closing the underlying client during shutdown of the Starlite application.\n\n### ORM Configuration\n\nA SQLAlchemy declarative base class that includes:\n\n- a mapping of the builtin `UUID` type to the postgresql dialect UUID type.\n- an `id` column\n- a `created` timestamp column\n- an `updated` timestamp column\n- an automated `__tablename__` attribute\n- a `from_dto()` class method, to ease construction of model types from DTO objects.\n\nWe also add:\n\n- a `before_flush` event listener that ensures that the `updated` timestamp is touched on instances\n  on their way into the database.\n- a constraint naming convention so that index and constraint names are automatically generated.\n\n### Service object\n\nA Service object that integrates with the Repository ABC and provides standard logic for typical\noperations.\n\n### Settings\n\nConfiguration by environment.\n\n## Contributing\n\nAll contributions big or small are welcome and appreciated! Please check out `CONTRIBUTING.md` for\nspecific information about configuring your environment and workflows used by this project.\n',
    'author': 'Peter Schutt',
    'author_email': 'peter.github@proton.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/topsport-com-au/starlite-saqlalchemy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
