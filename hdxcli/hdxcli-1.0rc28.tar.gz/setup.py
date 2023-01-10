# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hdx_cli',
 'hdx_cli.cli_interface',
 'hdx_cli.cli_interface.common',
 'hdx_cli.cli_interface.dictionary',
 'hdx_cli.cli_interface.function',
 'hdx_cli.cli_interface.job',
 'hdx_cli.cli_interface.migrate',
 'hdx_cli.cli_interface.profile',
 'hdx_cli.cli_interface.project',
 'hdx_cli.cli_interface.public',
 'hdx_cli.cli_interface.set',
 'hdx_cli.cli_interface.sources',
 'hdx_cli.cli_interface.table',
 'hdx_cli.cli_interface.transform',
 'hdx_cli.library_api',
 'hdx_cli.library_api.common',
 'hdx_cli.library_api.userdata',
 'hdx_cli.library_api.utility']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'requests>=2.28.1,<3.0.0', 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['hdxcli = hdx_cli.main:main']}

setup_kwargs = {
    'name': 'hdxcli',
    'version': '1.0rc28',
    'description': 'Hydrolix command line utility to do CRUD operations on projects, tables, transforms and other resources in Hydrolix clusters',
    'long_description': '[![](images/hdxcli.png)](https://github.com/hydrolix/hdx-cli)\n\n\n`hdxcli` is a command-line tool to work with hydrolix projects and tables\ninteractively.\n\nCommon operations such as CRUD operations on projects/tables/transforms \nand others  can be performed.\n\n# Hdx-cli installation\n\nYou can install `hdxcli` from pip:\n\n```shell\npip install hdxcli\n```\n\n# Using hdxcli command-line program\n\n`hdxcli` supports multiple profiles. You can use a default profile or\nuse the `--profile` option to operate on a non-default profile.\n\nWhen trying to invoke a command, if a login to the server is necessary, \na prompt will be shown and the token will be cached.\n\n\n# Command-line tool organization\n\nThe tool is organized, mostly with the general invocation form of:\n\n```shell\nhdxcli <resource> [<subresource...] <verb> [<resource_name>]\n```\n\nTable and project resources have defaults that depend on the profile you are working with,\nso they can be omitted if you used the `set` command.\n\nFor all other resources, you can use `--transform`, `--dictionary`, etc. Please see the\ncommand line help for more information.\n\n## Projects, tables and transforms\n\nThe basic operations you can do with these resources are:\n\n- list them\n- create a new resource\n- delete an existing resource\n- modify an existing resource\n- show a resource in raw json format\n- show settings from a resource\n- write a setting\n- show a single setting\n\n## Working with transforms and batch jobs\n\nIn order to use a transforms, you need to:\n\n1. create a transform\n\n\n``` shell\nhdxcli transform create -f atransform.json atransform\n```\n\nWhere atransform.json is a local file and atransform is the \nname for the transform that will be uploaded to the cluster. \nRemember that a transform is applied to a table in a project, \nso whatever you `set` with the \ncommand-line tool will be the target of your transform.\n\nIf you want to override it, do:\n\n``` shell\nhdxcli --project <the-project> --table <the-table> transform create -f atransform.json atransform\n```\n\n\n2. ingest a batch job\n\n``` shell\nhdxcli job batch ingest <job-name> <job-url>\n```\n\nThe job-name is the job name you will see if you list the job batch. job url can be either a local url or a url\nto a bucket *for which the cluster has at lease read access to*.\n\n\n## Listing and showing your profiles \n\nListing profiles:\n\n\n``` shell\nhdxcli profile list\n```\n\nShogin default profile\n\n``` shell\nhdxcli profile show\n```\n\n\n\n## FAQ: Common operations\n\n### Showing help \n\nIn order to see what you can do with the tool:\n\n``` shell\nhdxcli --help\n```\n\n### Listing resources\n\nTo list projects:\n\n``` shell\nhdxcli project list\n```\n\nTo list resources on a project:\n\n``` shell\nhdxcli --project <project-name> table list\n```\n\n\nYou can avoid repeating the project and table name by using the `set` command:\n\n\n### Set/unset project and table\n\n``` shell\nhdxcli set <your-project> <your-table>\n```\n\nSubsequent operations will be applied to the project and table. If you want to `unset`\nit, just do:\n\n``` shell\nhdxcli unset\n```\n\n\n### Creating resources\n\n``` shell\nhdxcli project create <project-name>\n```\n\n\n### Peforming operations against another server\n\nIf you want to use `hdxcli` against another server, use `--profile` option:\n\n\n### Working with resource settings\n\nShow settings for a resource:\n\n``` shell\nhdxcli project <myprojectname> settings\n```\n\n``` shell\nhdxcli table <mytablename> settings\n```\n\n``` shell\nhdxcli --transform <mytransform transform settings\n```\n\n\nModify a setting:\n\n``` shell\nhdxcli table <mytablename> settings key value\n```\n\nShow a single setting:\n\n``` shell\nhdxcli table <mytablename> settings key value\n```\n\n\n\n### Getting help for subcommands\n\nCheck which commands are available for each resource by typing:\n\n\n```\nhdxcli [<resource>...] [<verb>] --help\n```\n',
    'author': 'German Diago Gomez',
    'author_email': 'german@hydrolix.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
