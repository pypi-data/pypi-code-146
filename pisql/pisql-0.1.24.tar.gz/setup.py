# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pisql', 'pisql.cli', 'pisql.core', 'pisql.utils']

package_data = \
{'': ['*'], 'pisql': ['assets/*', 'assets/data/*', 'assets/sql/*']}

install_requires = \
['iotree==0.1.15', 'polars>=0.15.13,<0.16.0', 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['pisql = pisql.main:app']}

setup_kwargs = {
    'name': 'pisql',
    'version': '0.1.24',
    'description': '',
    'long_description': '# What is pisql ?\n\npisql is a mix of a command line tool and a small python library to interact with a [Sybase ASE][^1] database.  \nIt so happens, that I have to work with a Sybase ASE database and I wanted to have a tool to interact with it.  \n\n## But why ?\n\nThe reason I built this is fairly simple although frustrating:\n\n* My company has tight control over what gets installed on the workstations\n* My company hasn\'t bought the SQL Anywhere drivers for ASE on top of ASE itself as of today\n* The only way I have to interact with the database is through a [very old and ugly piece of software called "sqlDbx"][^2].\n* I wanted to have scripting and automation capabilities that the interface couldn\'t provide, but that bash/powershell/python could.\n\n## What is it ?\n\npisql is, for the CLI part, a [rich CLI wrapper][^3] around the barebones [isql][^4] command line tool that comes with the ASE installation every time.\n\nFor the python part, it\'s a small library that allows you to interact with the database through python code.\nYou can turn `.sql` files into dataframes ([pandas](https://pandas.pydata.org/) or [polars](pola.rs)), and further manipulate them.\nYou can use every tool you have in python to interact with the data, vizualize it, etc.\n\n## How do I use it ?\n\n### Installation\n\nYou can install pisql through pip:\n\n```bash\n    pip install pisql\n```\n\nAlthough I recommend `pipx`:\n\n```bash\n    pipx install pisql\n```\n\nThis works on Windows, Linux and MacOS.\n\n### Usage\n\n#### CLI\n\nThe CLI is fairly simple to use.\n\nTo execute a single .sql file, you can just use the `exec` command:\n\n```bash\n    pisql exec my_file.sql\n```\n\nwhich is also aliased to `pisql e my_file.sql` and `pisql x my_file.sql`.\n\nTo execute multiple .sql files, you can use what I call the "query mode" or "run mode", using either  \nthe symbols `q`, `run` or `::`. Once this more is activated, you can chain multiple executions together  \nby using the `++` or `//` commands:\n\n```bash\n    pisql q ++ file_one.sql file_two.sql file_three.sql\n```\n\nAn important feature of this mode, is that you can list both files and directories.\n\n\n```bash\n    pisql :: // file.sql some_dir other_file.sql\n```\n\nWhat happens then is that pisql will execute sequentially:\n\n* `file.sql` first\n* then all the `.sql` files in `some_dir` second\n* then `other_file.sql` last\n\nOne nice feature is the presence of rich progress bars like so (give example)\n\n**NB:** I haven\'t had the time to implement further recursion, so if you have a directory in `some_dir`, it will be ignored.\n\n#### Python\n\nWill explain in the next few days.\n\n## What\'s next ?\n\nI\'m currently working on a few things:\n\n* [ ] Implementing a config file subcommand to set the default database, user, etc.\n* [ ] Give more freedom to users to change the storage of the dataframes and config files\n* [ ] Build a semi ORM to interact with the database through python. Comes to mind the SELECT, WHERE, JOIN, etc. clauses.\n* [ ] Have a little templating feature, but nothing too fancy. I don\'t want to reinvent the wheel here.\n* [ ] Use Agg-Grid to have a  web interface to interact with the database. I\'m not sure how to do this yet, but I\'ll figure it out.\n\nHere\'s most of it for now ! I\'ll update this as I go.\n\n[^1]: https://www.sap.com/products/technology-platform/sybase-ase.html\n[^2]: http://www.sqldbx.com/\n[^3]:https://github.com/Textualize/rich\n[^4]:https://infocenter.sybase.com/help/index.jsp?topic=/com.sybase.infocenter.dc35456.1570/html/ocspsunx/X33477.htm',
    'author': 'Arno V',
    'author_email': 'arno@veletanlic.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
