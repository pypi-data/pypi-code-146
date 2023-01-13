# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dbt_serverless', 'dbt_serverless.config', 'dbt_serverless.lib']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'dbt-bigquery>=1.3.0,<2.0.0',
 'fastapi>=0.89.0,<0.90.0',
 'google-cloud-storage>=2.7.0,<3.0.0',
 'pulumi-gcp>=6.46.0,<7.0.0',
 'pulumi==3.33.1',
 'pydantic>=1.10.4,<2.0.0',
 'uvicorn>=0.20.0,<0.21.0']

setup_kwargs = {
    'name': 'dbt-serverless',
    'version': '0.1.2',
    'description': 'Project to deploy dbt as a serverless application in Cloud Run',
    'long_description': '# Serverless Endpoint for dbt runs\n\n\n[![GitHub Actions][github-actions-badge]](https://github.com/JeremyLG/dbt-serverless/actions)\n[![GitHub Actions][github-actions-terraform-badge]](https://github.com/JeremyLG/dbt-serverless/actions)\n[![Packaged with Poetry][poetry-badge]](https://python-poetry.org/)\n[![Code style: black][black-badge]](https://github.com/psf/black)\n[![Imports: isort][isort-badge]](https://pycqa.github.io/isort/)\n[![Type checked with mypy][mypy-badge]](https://github.com/python/mypy)\n[![codecov][codecov-badge]](https://codecov.io/github/JeremyLG/dbt-serverless)\n\n[![PyPI Latest Release](https://img.shields.io/pypi/v/dbt-serverless.svg)](https://pypi.org/project/dbt-serverless/)\n[![Package Status](https://img.shields.io/pypi/status/dbt-serverless.svg)](https://pypi.org/project/dbt-serverless/)\n[![License](https://img.shields.io/pypi/l/dbt-serverless.svg)](https://github.com/JeremyLG/dbt-serverless/blob/master/LICENSE.txt)\n\n[github-actions-badge]: https://github.com/JeremyLG/dbt-serverless/actions/workflows/python.yml/badge.svg\n[github-actions-terraform-badge]: https://github.com/JeremyLG/dbt-serverless/actions/workflows/terraform.yml/badge.svg\n[black-badge]: https://img.shields.io/badge/code%20style-black-000000.svg\n[isort-badge]: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336\n[mypy-badge]: https://www.mypy-lang.org/static/mypy_badge.svg\n[poetry-badge]: https://img.shields.io/badge/packaging-poetry-cyan.svg\n[codecov-badge]: https://codecov.io/github/JeremyLG/dbt-serverless/branch/master/graph/badge.svg\n\nThe goal of this project is to avoid the need of an Airflow server in order to schedule dbt tasks like runs, snapshots, docs...\n\nIt currently encapsulate few dbt commands into a FastAPI server which can be deployed on Cloud Run in a serverless fashion. That way we reduce costs as Cloud Run is terribly cheap!\n\nYou can also test it locally or through Docker without it being serverless, but it doesn\'t make sense as you already have the dbt CLI for this.\n\n## Usage\n\nYou\'ll need to make use of Google ADC (Authentification Default Credentials). Meaning either :\n- gcloud cli already identified\n- or a deployment through a google product with a service account having the roles/bigquery.admin\n- or a GOOGLE_APPLICATION_CREDENTIALS env variable for a specific local keyfile \n\n### Local deployment\n\n#### With pip\n\n```bash\npip install dbt-serverless\npython run uvicorn dbt_serverless.main:app --host 0.0.0.0 --port 8080 --reload\n```\n\n#### With poetry\n\n```bash\npoetry add dbt-serverless\npoetry run uvicorn dbt_serverless.main:app --host 0.0.0.0 --port 8080 --reload\n```\n\n\n### Docker deployment\nSimple docker image to build dbt-serverless for local or cloud run testing (for example).\n\n```docker\nARG build_for=linux/amd64\n\nFROM --platform=$build_for python:3.10-slim-bullseye\n\nARG DBT_PROJECT\nARG PROFILES_DIR\n\nWORKDIR /usr/app\n\nRUN pip install --no-cache-dir --upgrade pip && \\\n    pip install --no-cache-dir dbt-serverless\n\nCOPY ${DBT_PROJECT}/ ${PROFILES_DIR}/profiles.yml ${DBT_PROJECT}/\n\nENTRYPOINT ["uvicorn", "dbt_serverless.main:app", "--host", "0.0.0.0", "--port", "8080"]\n```\n\nIf you\'re not on a Google product (like Cloud Run), you will need to specify google creds at docker runtime.\n\nFor example you can add these cli parameters at runtime, if you\'re testing and deploying it locally :\n```bash\n    -v "$(HOME)/.config/gcloud:/gcp/config:ro" \\\n    -v /gcp/config/logs \\\n    --env CLOUDSDK_CONFIG=/gcp/config \\\n    --env GOOGLE_APPLICATION_CREDENTIALS=/gcp/config/application_default_credentials.json \\\n    --env GOOGLE_CLOUD_PROJECT=$(PROJECT_ID) \\\n```\n\n',
    'author': 'JeremyLG',
    'author_email': 'jeremy.le-gall@hotmail.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/JeremyLG/dbt-serverless',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
