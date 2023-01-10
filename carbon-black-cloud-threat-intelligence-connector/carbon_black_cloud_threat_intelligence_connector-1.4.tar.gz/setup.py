# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cbc_importer',
 'cbc_importer.cli',
 'cbc_importer.stix_parsers',
 'cbc_importer.stix_parsers.v1',
 'cbc_importer.stix_parsers.v2']

package_data = \
{'': ['*']}

install_requires = \
['arrow==1.2.2',
 'cabby==0.1.23',
 'carbon-black-cloud-sdk==1.3.5',
 'click==8.0.4',
 'stix-validator==2.5.1',
 'stix2-patterns==2.0.0',
 'stix2-validator==3.0.2',
 'stix2==3.0.1',
 'stix==1.2.0.11',
 'taxii2-client==2.3.0',
 'typer==0.4.0',
 'validators==0.18.2']

entry_points = \
{'console_scripts': ['cbc-threat-intel = cbc_importer.cli.connector:cli',
                     'cbc-threat-intel-wizard = cbc_importer.cli.wizard:cli']}

setup_kwargs = {
    'name': 'carbon-black-cloud-threat-intelligence-connector',
    'version': '1.4',
    'description': 'Carbon Black Cloud Threat Intelligence Connector',
    'long_description': '# Threat Intelligence Connector for Carbon Black Cloud\n\nThis is a python project that can be used for ingesting Threat Intelligence from various STIX Feeds. The current supported versions of STIX Feeds are 1.x, 2.0 and 2.1.\nIt supports python >= 3.8\n\n[![Coverage Status](https://coveralls.io/repos/github/carbonblack/carbon-black-cloud-threat-intelligence-connector/badge.svg?t=TczX1a)](https://coveralls.io/github/carbonblack/carbon-black-cloud-threat-intelligence-connector)\n[![Codeship Status for carbonblack/carbon-black-cloud-threat-intelligence-connector](https://app.codeship.com/projects/73a21e3d-2c23-4fa8-a611-ada9d9849f2c/status?branch=main)](https://app.codeship.com/projects/456985)\n\n## Installation\n\n```shell-session\n$ pip install carbon-black-cloud-threat-intelligence-connector\n$ cbc-threat-intel --help\nUsage: cbc-threat-intel [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  create-feed       Creates a feed in CBC\n  create-watchlist  Creates a Watchlist in CBC (from already created feed)\n  process-file      Process and import a single STIX content file into...\n  process-server    Process and import a TAXII Server (2.0/2.1/1.x)\n  version           Shows the version of the connector\n```\n\n## Documentation\n\nVisit the [developer network of Carbon Black Cloud](https://developer.carbonblack.com/reference/carbon-black-cloud/integrations/threat-intelligence-connector/) for more information of how to use the connector.\n\n## Developing the connector\n\nWe rely on pull requests to keep this project maintained. By participating in this project, you agree to abide by the VMware [code of conduct](CODE-OF-CONDUCT.md).\n\n### Setup\n\nIt is recommended to use Python3.8 / Python3.9 version for that project, assuming that you installed the deps with either virtualenv or poetry.\n\nFor a good code quality make sure to install the hooks from `pre-commit` as well.\n\n```shell-session\n$ pre-commit install\n```\n\n### Installation\n\nClone the repository\n\n```bash\n$ git clone https://github.com/carbonblack/carbon-black-cloud-threat-intelligence-connector.git\n$ cd carbon-black-cloud-threat-intelligence-connector/\n```\n\nYou can install this connector either via Poetry or using the `virtualenv`.\n\n#### Using [Poetry](https://python-poetry.org/docs/)\n\nYou will need to [install poetry](https://python-poetry.org/docs/#installation) first.\n\nTo install the connector run:\n\n```shell-session\n$ poetry install\n```\n\n#### Using [virtualenv](https://virtualenv.pypa.io/en/latest/)\n\nYou will need to [install virtualenv](https://virtualenv.pypa.io/en/latest/installation.html) first.\n\n```bash\n$ virtualenv venv\n...\n$ source ./venv/bin/activate\n(venv) $ pip install -r requirements.txt\n```\n\n### Tests\n\nThe tests can be run with the following command:\n\n```shell-session\n$ pytest ./tests/unit/\n```\nFor running the performance tests check out the [README](tests/performance/README.md)\n\n### Support\n\n1. View all API and integration offerings on the [Developer Network](https://developer.carbonblack.com) along with reference documentation, video tutorials, and how-to guides.\n2. Use the [Developer Community Forum](https://community.carbonblack.com/) to discuss issues and get answers from other API developers in the Carbon Black Community.\n3. Create a github issue for bugs and change requests or create a ticket with [Carbon Black Support](http://carbonblack.com/resources/support/).\n\n### Submitting a PR\n\nIt is strongly recommended to have written tests and documentation for your changes before submitting a PR to the project. Make sure to write good commit messages as well.\n',
    'author': 'Dimitar Ganev',
    'author_email': 'dganev@vmware.com',
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
