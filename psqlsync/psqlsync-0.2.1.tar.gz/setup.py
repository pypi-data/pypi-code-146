# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['psqlsync', 'psqlsync.ghmoteqlync']

package_data = \
{'': ['*']}

install_requires = \
['psycopg2-binary>=2.9.2,<3.0.0', 'tomli>=2.0.1,<3.0.0']

extras_require = \
{'dirgh': ['dirgh>=0.2.0,<0.3.0', 'trio>=0.20.0,<0.23.0']}

entry_points = \
{'console_scripts': ['prep = psqlsync.ghremote.cli:run',
                     'psqlsync = psqlsync.cli:run']}

setup_kwargs = {
    'name': 'psqlsync',
    'version': '0.2.1',
    'description': 'Tool to create basic PostgreSQL backups and restore them from local files.',
    'long_description': '# PostgreSQLSync\n\nTool to create basic PostgreSQL dumps and restore them from local files. \n\nDon\'t use this for production-critical backups, SQL dumps (the method used by this library) are neither efficient nor safe for that purpose. Instead, use a tool like [Barman](https://pgbarman.org/).\n\n### Based on [postgres_manage_python](https://github.com/valferon/postgres-manage-python) by [valferon](https://github.com/valferon). Thanks to him for the core logic.\n\nThis was forked to create a more minimal and maintainable package for the specific use case of syncing a populated testing database.\n\n## Getting Started\n\n### Setup\n\nThis library requires the installation of a PostgreSQL client, as it runs pg_restore and pg_dump directly from the command line, as there are no Python bindings for these functions, unfortunately. Use the below instructions to install the PostgreSQL 14 client ([instructions from here](https://wiki.postgresql.org/wiki/Apt)). Note that this installs some basic tools (see the first line of the shell below), replace them at your discretion if e.g. you don\'t want to bloat your container environment.\n\n```shell\nsudo apt install curl ca-certificates gnupg lsb-release\ncurl https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/apt.postgresql.org.gpg >/dev/null\nsudo sh -c \'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list\'\nsudo apt update\nsudo apt install postgresql-client-14\n```\n\n* Create configuration file (ie. sample.toml)\n```toml\n[setup]\nstorage_engine= "LOCAL"\n\n[local_storage]\npath = "./backups/"\n\n[postgresql]\nhost="<your_psql_addr(probably 127.0.0.1)>"\nport="<your_psql_port(probably 5432)>"\ndb="<your_db_name>"\nuser="<your_username>"\npassword="<your_password>"\n```\n\n\n### Usage\n\n* List databases on a PostgreSQL server\n\n      psqlsync --config sample.toml --action list_dbs\n\n* Create database backup and store it (based on config file details)\n\n      psqlsync --config sample.toml --action backup --verbose\n\n* List previously created database backups available on storage engine\n\n      psqlsync --config sample.toml --action list\n\n* Restore previously created database backups available on storage engine (check available dates with *list* action, it matches the time string, so any unique part of the string suffices)\n\n      pslsync --config sample.toml --action restore --date 2021\n\n* Restore previously created database backups into a new destination database\n\n      pslsync --config sample.toml --action restore --date 20211219-14 --dest-db new_DB_name\n\n* Enter password in prompt, so it does not have to be stored in plaintext in the config file\n\n      pslsync --config sample.toml --action backup --prompt-pass\n      Password for database: \n\n\n### Command help\n```\nusage: psqlsync [-h] --action action [--time YYYYMMdd-HHmmss] [--dest-db dest_db] [--verbose] --config CONFIG\n                [--prompt-pass]\n\npsqlsync\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --action action       \'list\' (backups), \'list_dbs\' (available dbs), \'restore\' (requires --time), \'backup\'\n  --time YYYYMMdd-HHmmss\n                        Time to use for restore (show with --action list). If unique, will smart match. (If\n                        there\'s just one backup matching YYYMM, providing that is enough)\n  --dest-db dest_db     Name of the new restored database\n  --verbose             Verbose output\n  --config CONFIG       Database configuration file path (.toml)\n  --prompt-pass         Show a password prompt instead of the password defined in the config.\n```\n\n\n### Run programmatically\n\nThe `backup` and `restore` action have been seperated into easily callable Python functions in `psqlsync.actions`. You can import this module and call these functions from your Python code.\n\n\n## Authors\n\n* **Tip ten Brink**\n* **[Val Feron](https://github.com/valferon)** - *Initial work* \n\n\n## License\n\nThe original code, created by [valferon](https://github.com/valferon) in the [postgres_manage_python repository](https://github.com/valferon/postgres-manage-python), is licensed under the MIT License. This project as a whole, most notably my original code, is licensed under the Apache License v2.0.\n',
    'author': 'Tip ten Brink',
    'author_email': '75669206+tiptenbrink@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
