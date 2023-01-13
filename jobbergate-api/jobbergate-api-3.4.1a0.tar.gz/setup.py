# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jobbergate_api',
 'jobbergate_api.apps',
 'jobbergate_api.apps.applications',
 'jobbergate_api.apps.job_scripts',
 'jobbergate_api.apps.job_submissions',
 'jobbergate_api.tests',
 'jobbergate_api.tests.apps',
 'jobbergate_api.tests.apps.applications',
 'jobbergate_api.tests.apps.job_scripts',
 'jobbergate_api.tests.apps.job_submissions',
 'jobbergate_api.tests.integration']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.0.3,<4.0.0',
 'PyYAML>=6.0,<7.0',
 'alembic>=1.7.5,<2.0.0',
 'armasec>=0.11.0,<0.12.0',
 'asyncpg>=0.22.0,<0.23.0',
 'bidict>=0.22.0,<0.23.0',
 'boto3>=1.17.51,<2.0.0',
 'databases[postgresql]>=0.5.5,<0.6.0',
 'email_validator>=1.1.0,<2.0.0',
 'fastapi>=0.68.0,<0.69.0',
 'file-storehouse==0.5.0',
 'loguru>=0.6.0,<0.7.0',
 'passlib>=1.7.2,<2.0.0',
 'py-buzz>=3.2.1,<4.0.0',
 'python-dotenv>=0.20.0,<0.21.0',
 'python-multipart>=0.0.5,<0.0.6',
 'sendgrid>=6.9.7,<7.0.0',
 'sentry-sdk>=1.5.0,<2.0.0',
 'toml>=0.10.2,<0.11.0',
 'typer>=0.4.0,<0.5.0',
 'uvicorn>=0.15.0,<0.16.0',
 'yarl>=1.7.2,<2.0.0']

entry_points = \
{'console_scripts': ['dev-tools = dev_tools:app']}

setup_kwargs = {
    'name': 'jobbergate-api',
    'version': '3.4.1a0',
    'description': 'Jobbergate API',
    'long_description': '================\n Jobbergate API\n================\n\n\nThe Jobbergate API provides a RESTful interface over the Jobbergate data and is used\nby both the ``jobbergate-agent`` and the ``jobbergate-cli`` to view and manage the\nJobbergate resources.\n\nJobbergate API is a Python project implemented with\n`FastAPI <https://fastapi.tiangolo.com/>`_. Its dependencies and environment are\nmanaged by `Poetry <https://python-poetry.org/>`_.\n\nIt integrates with an OIDC server to provide identity and auth for its endpoints.\n\nSee also:\n\n* `jobbergate-cli <https://github.com/omnivector-solutions/jobbergate/jobbergate-cli>`_\n\nLicense\n-------\n* `MIT <LICENSE>`_\n\n\nCopyright\n---------\n* Copyright (c) 2020 OmniVector Solutions <info@omnivector.solutions>\n',
    'author': 'Omnivector Solutions',
    'author_email': 'info@omnivector.solutions',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/omnivector-solutions/jobbergate',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
