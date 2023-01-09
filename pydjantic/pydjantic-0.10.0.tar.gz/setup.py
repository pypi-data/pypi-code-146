# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydjantic']

package_data = \
{'': ['*']}

install_requires = \
['dj-database-url>=0.5.0,<0.6.0', 'pydantic[dotenv]>=1.8.1,<2.0.0']

setup_kwargs = {
    'name': 'pydjantic',
    'version': '0.10.0',
    'description': 'Pydantic Settings for Django',
    'long_description': '# pydjantic\n[![Build Status](https://github.com/ErhoSen/pydjantic/actions/workflows/main.yml/badge.svg)](https://github.com/ErhoSen/pydjantic/actions)\n[![codecov](https://codecov.io/gh/ErhoSen/pydjantic/branch/master/graph/badge.svg?token=BW5A0V3CR3)](https://codecov.io/gh/ErhoSen/pydjantic)\n[![pypi](https://img.shields.io/pypi/v/pydjantic.svg)](https://pypi.org/project/pydjantic/)\n[![versions](https://img.shields.io/pypi/pyversions/pydjantic.svg)](https://github.com/ErhoSen/pydjantic)\n[![license](https://img.shields.io/github/license/erhosen/pydjantic.svg)](https://github.com/ErhoSen/pydjantic/blob/master/LICENSE)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nUse Pydantic Settings in your Django application.\n\n![Pydjantc django settings](https://github.com/ErhoSen/pydjantic/raw/master/images/pydjantic.png "Pydjantc django settings")\n\n## Introduction\n\nIf you are tired of the mess in your Django Settings - I feel your pain:\n* Ridiculously long `settings.py` file, with ASCII-art separation\n* `from common import *` Python [anti-pattern](https://www.geeksforgeeks.org/why-import-star-in-python-is-a-bad-idea/)\n* `try: <import> except: ImportError` Python [anti-pattern](https://stackoverflow.com/questions/14050281/how-to-check-if-a-python-module-exists-without-importing-it)\n* `base.py`, `production.py`, `local.py`, `domain.py` - bunch of unrelated modules that override each other\n* [django-environ](https://github.com/joke2k/django-environ) library, that do even worse...\n\nOn the other hand we have [Pydantic Settings](https://pydantic-docs.helpmanual.io/usage/settings/),\nwhich is de-facto standard for all non-django projects.\n\nIf you love Pydantic settings management approach, **Pydjantic** is a right tool for you.\n\n**Pydjantic** allows you to define your settings in familiar way - just inherit from `BaseSettings`:\n```py\nfrom typing import List\n\nfrom pydantic import BaseSettings, Field\nfrom pydantic.fields import Undefined\nfrom pydjantic import to_django\n\nclass GeneralSettings(BaseSettings):\n    SECRET_KEY: str = Field(default=Undefined, env=\'DJANGO_SECRET_KEY\')\n    DEBUG: bool = Field(default=False, env=\'DEBUG\')\n    INSTALLED_APPS: List[str] = [\n        \'django.contrib.admin\',\n        \'django.contrib.auth\',\n    ]\n    LANGUAGE_CODE: str = \'en-us\'\n    USE_TZ: bool = True\n\n\nclass StaticSettings(BaseSettings):\n    STATIC_URL: str = \'/static/\'\n    STATIC_ROOT: str = \'staticfiles\'\n\n\nclass SentrySettings(BaseSettings):\n    SENTRY_DSN: str = Field(default=Undefined, env=\'SENTRY_DSN\')\n\n\nclass ProjectSettings(GeneralSettings, StaticSettings, SentrySettings):\n    pass\n\n\nto_django(ProjectSettings())\n```\nYou can create as many classes/modules as you want, to achieve perfect settings\' management.\nDivide your settings by domains, and then create final `ProjectSettings` class, that inherits from these domains.\n\nProvide the instance of `ProjectSettings` to `to_django` function.\nThat\'s all, your django settings will work as expected.\n\n## Installation\n\nInstall using `pip install -U pydjantic` or `poetry add pydjantic`.\n\n## Example\nIn the `/demo` directory you can find a [working Django app](https://github.com/ErhoSen/pydjantic/tree/master/demo) with [pydjantic settings](https://github.com/ErhoSen/pydjantic/blob/master/demo/demo/settings.py).\n\n## Database configuration\n\n**Pydjantic** comes with a special helper for managing DB configs - `BaseDBConfig`. See example below:\n```python\nfrom pydantic import Field, PostgresDsn\nfrom pydjantic import BaseDBConfig\n\n\nclass DatabaseConfig(BaseDBConfig):\n    default: PostgresDsn = Field(default="postgres://user:password@hostname:5432/dbname", env="DATABASE_URL")\n\ndb_settings = DatabaseConfig()\nassert db_settings.default == {\n    \'CONN_MAX_AGE\': 0,\n    \'ENGINE\': \'django.db.backends.postgresql_psycopg2\',\n    \'HOST\': \'hostname\',\n    \'NAME\': \'dbname\',\n    \'PASSWORD\': \'password\',\n    \'PORT\': 5432,\n    \'USER\': \'user\',\n}\n```\n\nAlso, you can define database configurations directly:\n```python\nfrom pydantic import BaseSettings, Field\n\nclass PostgresDB(BaseSettings):\n    ENGINE: str = \'django.db.backends.postgresql_psycopg2\'\n    HOST: str = Field(default=\'localhost\', env=\'DATABASE_HOST\')\n    NAME: str = Field(default=\'dbname\', env=\'DATABASE_NAME\')\n    PASSWORD: str = Field(default=\'password\', env=\'DATABASE_PASSWORD\')\n    PORT: int = Field(default=5432, env=\'DATABASE_PORT\')\n    USER: str = Field(default=\'user\', env=\'DATABASE_USER\')\n    OPTIONS: dict = Field(default={}, env=\'DATABASE_OPTIONS\')\n    CONN_MAX_AGE: int = Field(default=0, env=\'DATABASE_CONN_MAX_AGE\')\n\nclass DatabaseConfig(BaseSettings):\n    default = PostgresDB()\n```\n\nOr mix these approaches:\n```python\nclass DatabaseConfig(BaseDBConfig):\n    default = Field(default="postgres://user:password@hostname:5432/dbname")\n    replica = PostgresDB()\n```\n\nFor more examples see [tests](tests/test_db_config.py).\n\nTransformation from dsn to django format is done by [dj-database-url](https://pypi.org/project/dj-database-url/) library.\n',
    'author': 'Vladimir Vyazovetskov',
    'author_email': 'erhosen@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ErhoSen/pydjantic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
