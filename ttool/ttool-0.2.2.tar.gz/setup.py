# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ttool', 'ttool.jira_utils']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'dacite>=1.7.0,<2.0.0',
 'docopt>=0.6.2,<0.7.0',
 'inquirer>=3.1.2,<4.0.0',
 'jira>=3.4.1,<4.0.0',
 'requests-toolbelt>=0.10.1,<0.11.0',
 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['ttool = ttool.main:app']}

setup_kwargs = {
    'name': 'ttool',
    'version': '0.2.2',
    'description': 'Tugys utils tools',
    'long_description': "# TTOOL (Tugy Tools)\n\nThis Repository is for utils that me, Tugy, thought that will be usefull.\n\nAuthor: [Tugy](https://github.com/IamTugy) | Github Repo: [tugytools](https://github.com/IamTugy/tugytools)\n\n## Installation:\n    $ pip install ttool\n## Packages:\n### Jira:\nTo use the Jira utils you need to create 2 Global variables:\n`JIRA_API_TOKEN` and `JIRA_MAIL`.\nGet your `JIRA_API_TOKEN` [here](https://id.atlassian.com/manage-profile/security/api-tokens).\n\nYour `JIRA_MAIL` should store your jira mail ofc..\n\nI suggest that you store this values in `$HOME/.bashrc` or `$HOME/.aliases` if you have one.\n\n    $ ttool jira --help\n\n    Usage: ttool jira [OPTIONS] COMMAND [ARGS]...\n\n    Options:\n      --help  Show this message and exit.\n    \n    Commands:\n      checkout  Checkout/Print your chosen jira issue with...\n      setup     Set up your jira configurations.\n\n#### The Setup Command\nTo setup a local config file to store your jira project and host.\n\n    $ ttool jira setup --help\n\n    Usage: ttool jira setup [OPTIONS]\n\n      Set up your jira configurations.\n\n    Options:\n      --help  Show this message and exit.\n\n#### The Checkout Command:\nIt really annoyed me every time to copy the key and description from the jira and create indicative branch names.\nSo this command let you pick a ticket of yours from the jira in the CLI, and then checkout to a branch with this syntax:\n`ISSUE-123/My-issue-description`\n\n    $ ttool jira checkout --help\n    \n    Usage: ttool jira checkout [OPTIONS]\n    \n      Checkout/Print your chosen jira issue with 'ISSUE-ID/the-issue-summery'\n      format. use --print to print the branch name without checkout\n    \n    Options:\n      --print / --no-print  [default: no-print]\n      --help                Show this message and exit.\n",
    'author': 'IamTugy',
    'author_email': 'tugmica@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
