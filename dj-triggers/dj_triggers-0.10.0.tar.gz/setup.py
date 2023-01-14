# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['triggers', 'triggers.migrations']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3', 'celery>=4.4', 'django-polymorphic>=3.0.0,<4.0.0']

setup_kwargs = {
    'name': 'dj-triggers',
    'version': '0.10.0',
    'description': '',
    'long_description': '# django-triggers\n\n## Development\n\n### Run a django-admin command, e.g. `makemigrations`\n```shell\npoetry run python -m django makemigrations --settings=tests.app.settings\n```\n\n### Run isort\n```shell\npoetry run isort triggers tests\n```\n### Run flake8\n```shell\npoetry run flake8 triggers tests\n```\n### Run mypy\n```shell\npoetry run mypy triggers tests\n```\n### Run pytest\n```shell\npoetry run pytest\n```\n',
    'author': 'None',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/cockpithq/django-triggers',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
