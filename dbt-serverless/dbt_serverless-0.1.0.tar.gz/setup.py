# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dbt_serverless', 'dbt_serverless.lib']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'dbt-bigquery>=1.3.0,<2.0.0',
 'fastapi>=0.89.0,<0.90.0',
 'google-cloud-storage>=2.7.0,<3.0.0',
 'pydantic>=1.10.4,<2.0.0',
 'uvicorn>=0.20.0,<0.21.0']

entry_points = \
{'console_scripts': ['fact = fact.cli:app']}

setup_kwargs = {
    'name': 'dbt-serverless',
    'version': '0.1.0',
    'description': 'Test project PYPI publication for dbt serverless',
    'long_description': '# Serverless Endpoint for dbt runs\n\n\n[![GitHub Actions][github-actions-badge]](https://github.com/JeremyLG/dbt-serverless/actions)\n[![GitHub Actions][github-actions-terraform-badge]](https://github.com/JeremyLG/dbt-serverless/actions)\n[![Packaged with Poetry][poetry-badge]](https://python-poetry.org/)\n[![Code style: black][black-badge]](https://github.com/psf/black)\n[![Imports: isort][isort-badge]](https://pycqa.github.io/isort/)\n[![Type checked with mypy][mypy-badge]](https://github.com/python/mypy)\n[![codecov][codecov-badge]](https://codecov.io/github/JeremyLG/dbt-serverless)\n\n[![PyPI Latest Release](https://img.shields.io/pypi/v/dbt-serverless.svg)](https://pypi.org/project/dbt-serverless/)\n[![Package Status](https://img.shields.io/pypi/status/dbt-serverless.svg)](https://pypi.org/project/dbt-serverless/)\n[![License](https://img.shields.io/pypi/l/dbt-serverless.svg)](https://github.com/JeremyLG/dbt-serverless/blob/master/LICENSE)\n\n[github-actions-badge]: https://github.com/JeremyLG/dbt-serverless/actions/workflows/python.yml/badge.svg\n[github-actions-terraform-badge]: https://github.com/JeremyLG/dbt-serverless/actions/workflows/terraform.yml/badge.svg\n[black-badge]: https://img.shields.io/badge/code%20style-black-000000.svg\n[isort-badge]: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336\n[mypy-badge]: https://www.mypy-lang.org/static/mypy_badge.svg\n[poetry-badge]: https://img.shields.io/badge/packaging-poetry-cyan.svg\n[codecov-badge]: https://codecov.io/github/JeremyLG/dbt-serverless/branch/master/graph/badge.svg\n\nTO DOCUMENT\n',
    'author': 'JeremyLG',
    'author_email': 'jeremy.le-gall@hotmail.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/JeremyLG/dbt-serverless',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
