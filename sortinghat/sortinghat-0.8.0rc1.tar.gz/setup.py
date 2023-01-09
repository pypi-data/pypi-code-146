# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sortinghat',
 'sortinghat.app',
 'sortinghat.cli',
 'sortinghat.cli.client',
 'sortinghat.cli.cmds',
 'sortinghat.config',
 'sortinghat.core',
 'sortinghat.core.management',
 'sortinghat.core.management.commands',
 'sortinghat.core.migrations',
 'sortinghat.core.recommendations',
 'sortinghat.server',
 'sortinghat.utils',
 'tests',
 'tests.cli',
 'tests.rec']

package_data = \
{'': ['*'],
 'sortinghat.cli': ['templates/*'],
 'sortinghat.core': ['fixtures/*']}

install_requires = \
['Django>=3.2,<4.0',
 'Jinja2>=3.1.1,<4.0.0',
 'PyJWT>=2.4.0,<3.0.0',
 'click==7.1.1',
 'django-cors-headers>=3.7.0,<4.0.0',
 'django-graphql-jwt>=0.3.0,<0.4.0',
 'django-rq>=2.3.2,<3.0.0',
 'django-storages[google]>=1.13.2,<2.0.0',
 'django-treebeard>=4.5.1,<5.0.0',
 'graphene-django>=2.15,<3.0',
 'grimoirelab-toolkit>=0.3',
 'importlib-resources>=5.2.0,<6.0.0',
 'mysqlclient==2.0.3',
 'numpy==1.21.0',
 'pandas>=1.3.5,<2.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'requests>=2.7.0,<3.0.0',
 'rq>=1.4.0,<2.0.0',
 'setuptools>=65.5.0,<66.0.0',
 'sgqlc>=10.1,<11.0',
 'uWSGI>=2.0,<3.0']

entry_points = \
{'console_scripts': ['sortinghat = sortinghat.cli.sortinghat:sortinghat',
                     'sortinghat-admin = '
                     'sortinghat.server.sortinghat_admin:sortinghat_admin',
                     'sortinghatd = sortinghat.server.sortinghatd:sortinghatd',
                     'sortinghatw = sortinghat.server.sortinghatw:sortinghatw']}

setup_kwargs = {
    'name': 'sortinghat',
    'version': '0.8.0rc1',
    'description': 'A tool to manage identities.',
    'long_description': '# Sorting Hat [![tests](https://github.com/chaoss/grimoirelab-sortinghat/workflows/tests/badge.svg)](https://github.com/chaoss/grimoirelab-sortinghat/actions?query=workflow:tests+branch:master+event:push) [![PyPI version](https://badge.fury.io/py/sortinghat.svg)](https://badge.fury.io/py/sortinghat)\n\n## Description\n\nA tool to manage identities.\n\nSorting Hat maintains an SQL database of unique identities of communities members across (potentially) many different sources. Identities corresponding to the same real person can be merged in the same `individual`, with a unique uuid. For each individual, a profile can be defined, with the name and other data shown for the corresponding person by default.\n\nIn addition, each individual can be related to one or more affiliations, for different time periods. This will usually correspond to different organizations in which the person was employed during those time periods.\n\nSorting Hat is a part of the [GrimoireLab toolset](https://grimoirelab.github.io), which provides Python modules and scripts to analyze data sources with information about software development, and allows the production of interactive dashboards to visualize that information.\n\nIn the context of GrimoireLab, Sorting Hat is usually run after data is retrieved with [Perceval](https://github.com/chaoss/grimoirelab-perceval), to store the identities obtained into its database, and later merge them into individuals (and maybe affiliate them).\n\n\n## Requirements\n\n* Python >= 3.7\n* Poetry >= 1.1.0\n* MySQL >= 5.7 or MariaDB 10.0\n* Django = 3.1\n* Graphene-Django >= 2.0\n* uWSGI >= 2.0\n\nYou will also need some other libraries for running the tool, you can find the\nwhole list of dependencies in [pyproject.toml](pyproject.toml) file.\n\n\n## Installation\n\n### Getting the source code\n\nTo install from the source code you will need to clone the repository first:\n```\n$ git clone https://github.com/chaoss/grimoirelab-sortinghat\n$ cd grimoirelab-sortinghat\n```\n\n### Backend\n\n#### Prerequisites\n\n##### Poetry\n\nWe use [Poetry](https://python-poetry.org/docs/) for managing the project.\nYou can install it following [these steps](https://python-poetry.org/docs/#installation).\n\n##### mysql_config\n\nBefore you install SortingHat tool you might need to install `mysql_config`\ncommand. If you are using a Debian based distribution, this command can be\nfound either in `libmysqlclient-dev` or `libmariadbclient-dev` packages\n(depending on if you are using MySQL or MariaDB database server). You can\ninstall these packages in your system with the next commands:\n\n* **MySQL**\n\n```\n$ apt install libmysqlclient-dev\n```\n\n* **MariaDB**\n\n```\n$ apt install libmariadbclient-dev\n```\n\n#### Installation and configuration\n\n**Note**: these examples use `sortinghat.config.settings` configuration file.\nIn order to use that configuration you need to define the environment variable\n`SORTINGHAT_SECRET_KEY` with a secret. More info here:\nhttps://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-SECRET_KEY\n\n\nInstall the required dependencies (this will also create a virtual environment).\n```\n$ poetry install\n```\n\nActivate the virtual environment:\n```\n$ poetry shell\n```\n\nDatabase creation, apply migrations and fixtures, deploy static files,\nand create a superuser:\n```\n(.venv)$ sortinghat-admin --config sortinghat.config.settings setup\n```\n\n#### Running the backend\n\nRun SortingHat backend Django app:\n```\n(.venv)$ ./manage.py runserver --settings=sortinghat.config.settings\n```\n\n### Frontend\n\n#### Prerequisites\n\n##### yarn\n\nTo compile and run the frontend you will need to install `yarn` first.\nThe latest versions of `yarn` can only be installed with `npm` - which\nis distributed with [NodeJS](https://nodejs.org/en/download/).\n\nWhen you have `npm` installed, then run the next command to install `yarn`\non the system:\n\n```\nnpm install -g yarn\n```\n\nCheck the [official documentation](https://yarnpkg.com/getting-started)\nfor more information.\n\n#### Installation and configuration\n\nInstall the required dependencies\n```\n$ cd ui/\n$ yarn install\n```\n\n#### Running the frontend\n\nRun SortingHat frontend Vue app:\n```\n$ yarn serve\n```\n\n\n## SortingHat service\n\nStarting at version 0.8, SortingHat is released with a server app. The server has two\nmodes, `production` and `development`.\n\nWhen `production` mode is active, a WSGI app is served. The idea is to use a reverse\nproxy like NGINX or similar, that will be connected with the WSGI app to provide\nan interface HTTP.\n\nWhen `development` mode is active, an HTTP server is launched, so you can interact\ndirectly with SortingHat using HTTP requests. Take into account this mode is not\nsuitable nor safe for production.\n\nYou will need a django configuration file to run the service. The file must be accessible\nvia `PYTHONPATH` env variable. You can use the one delivered within the SortingHat\npackage (stored in `sortinghat/config` folder) and modify it with your parameters.\nFollowing examples will make use of that file.\n\nIn order to run the service for the first time, you need to execute the next commands:\n\nBuild the UI interface:\n```\n$ cd ui\n$ yarn build\n```\n\nSet a secret key:\n```\n$ export SORTINGHAT_SECRET_KEY="my-secret-key"\n```\n\nSet up the service creating a database, deploying static files,\nand adding a superuser to access the app:\n```\n$ sortinghat-admin --config sortinghat.config.settings setup\n```\n\nRun the server (use `--dev` flag for `development` mode):\n```\n$ sortinghatd --config sortinghat.config.settings\n```\n\nBy default, this runs a WSGI server in `127.0.0.1:9314`. The `--dev` flag runs\na server in `127.0.0.1:8000`.\n\nYou will also need to run some workers to execute tasks like recommendations\nor affiliation. To start a worker run the command:\n```\n$ sortinghatw --config sortinghat.config.settings\n```\n\n\n## Compatibility between versions\nSortingHat 0.7.x is not longer supported. Any database using this version will not work.\n\nSortingHat databases 0.7.x are no longer compatible. The `uidentities` table was renamed\nto `individuals`. The database schema changed in all tables to add the fields `created_at`\nand `last_modified`. Also in `domains`, `enrollments`, `identities`, `profiles` tables,\nthere are some specific changes to the column names:\n  * `domains`\n    * `organization_id` to `organization`\n  * `enrollments`\n    * `organization_id` to `organization`\n    * `uuid` to `individual`\n  * `identities`\n    * `uuid` to `individual`\n  * `profiles`\n    * `country_code` to `country`\n    * `uuid` to `individual`\n\nPlease update your database following the next steps:\n\n1. Use the script `utils/create_sh_0_7_fixture.py` to create the fixture\nJSON file\n   ```\n   $ python3 utils/create_sh_0_7_fixture.py test_sh -o test_sh_fixture.json\n   [2021-06-10 17:29:11,461][INFO] Start creating fixture file for test_sh\n   [2021-06-10 17:29:21,252][INFO] Fixture file created to test_sh_fixture.json\n   ```\n\n2. Create a new database.\n   ```\n   $ sortinghat-admin --config sortinghat.config.settings setup\n   ```\n\n4. Load fixture JSON file using Django\n   ```\n   $ python3 manage.py loaddata test_sh_fixture.json --settings= sortinghat.config.settings\n   Installed 148542 object(s) from 1 fixture(s)\n   ```\n\n## Running tests\n\nSortingHat comes with a comprehensive list of unit tests for both \nfrontend and backend.\n\n#### Backend test suite\n```\n(.venv)$ ./manage.py test --settings=config.settings.testing\n```\n\n#### Frontend test suite\n```\n$ cd ui/\n$ yarn test:unit\n```\n\n## License\n\nLicensed under GNU General Public License (GPL), version 3 or later.\n',
    'author': 'GrimoireLab Developers',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://chaoss.github.io/grimoirelab/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
