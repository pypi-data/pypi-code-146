# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jobbergate_cli',
 'jobbergate_cli.subapps',
 'jobbergate_cli.subapps.applications',
 'jobbergate_cli.subapps.clusters',
 'jobbergate_cli.subapps.job_scripts',
 'jobbergate_cli.subapps.job_submissions']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'boto3>=1.18.64,<2.0.0',
 'click>=8.0.1,<9.0.0',
 'httpx>=0.22.0,<0.23.0',
 'importlib-metadata>=4.2,<5.0',
 'inquirer>=2.7.0,<3.0.0',
 'loguru>=0.6.0,<0.7.0',
 'pendulum>=2.1.2,<3.0.0',
 'pep562>=1.1,<2.0',
 'py-buzz>=3.1.0,<4.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'pyperclip>=1.8.2,<2.0.0',
 'python-dotenv>=0.19.0,<0.20.0',
 'python-jose>=3.3.0,<4.0.0',
 'rich>=11.2.0,<12.0.0',
 'sentry-sdk>=1.4.3,<2.0.0',
 'typer>=0.4.0,<0.5.0',
 'yarl>=1.7.2,<2.0.0']

entry_points = \
{'console_scripts': ['jobbergate = jobbergate_cli.main:app']}

setup_kwargs = {
    'name': 'jobbergate-cli',
    'version': '3.4.1a0',
    'description': 'Jobbergate CLI Client',
    'long_description': '================\n Jobbergate CLI\n================\n\nThe Jobbergate CLI provides a command-line interface to view and manage the Jobbergate\nresources. It can be used to create Job Scripts from template and then submit them to\nthe Slurm cluster to which Jobbergate is connected.\n\nJobbergate CLI is a Python project implemented with the\n`Typer <https://typer.tiangolo.com/>`_ CLI builder library. Its dependencies and\nenvironment are managed by `Poetry <https://python-poetry.org/>`_.\n\nThe CLI has a rich help system that can be accessed by passing the ``--help`` flag to\nthe main command:\n\n.. code-block:: console\n\n   jobbergate job-scripts --help\n\n\nThere is also help and parameter guides for each of the subcommands that can be accessed\nby passing them the ``--help`` flag:\n\n.. code-block:: console\n\n   jobbergate job-scripts list --help\n\nSee also:\n\n* `jobbergate-api <https://github.com/omnivector-solutions/jobbergate/jobbergate-api>`_\n\nLicense\n-------\n* `MIT <LICENSE>`_\n\n\nCopyright\n---------\n* Copyright (c) 2020 OmniVector Solutions <info@omnivector.solutions>\n',
    'author': 'Omnivector Solutions',
    'author_email': 'info@omnivector.solutions',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/omnivector-solutions/jobbergate',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
