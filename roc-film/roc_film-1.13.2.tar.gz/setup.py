# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['roc',
 'roc.film',
 'roc.film.config',
 'roc.film.tasks',
 'roc.film.tests',
 'roc.film.tools']

package_data = \
{'': ['*']}

install_requires = \
['edds_process>=0.8.2',
 'h5py>=3.7,<4.0',
 'jinja2>=3.0,<4.0',
 'maser-tools>=0.1.3',
 'numpy!=1.19.5',
 'pandas>=1.3,<2.0',
 'poppy-core',
 'poppy-pop',
 'roc-dingo>=1.0,<2.0',
 'roc-idb>=1.0,<2.0',
 'roc-rap>=1.0,<2.0',
 'roc-rpl>=1.0,<2.0',
 'spacepy>=0.4,<0.5',
 'sqlalchemy>=1.4,<2.0',
 'xmltodict>=0.13,<0.14']

setup_kwargs = {
    'name': 'roc-film',
    'version': '1.13.2',
    'description': 'RPW FILe Maker (FILM): Plugin to make RPW L0, L1 and HK data files',
    'long_description': '# FILM PLUGIN README\n\n[![pipeline status](https://gitlab.obspm.fr/ROC/Pipelines/Plugins/FILM/badges/develop/pipeline.svg)](https://gitlab.obspm.fr/ROC/Pipelines/Plugins/FILM/pipelines)\n\nThis directory contains the source files of the Rpw FILe Maker (FILM), a plugin of the ROC pipelines dedicated to the RPW L0, L1 and HK files production.\n\nRPL has been developed with the [POPPY framework](https://poppy-framework.readthedocs.io/en/latest/).\n\n## Quickstart\n\n### Installation with pip\n\nTo install the plugin using pip:\n\n```\npip install roc-film --extra-index-url https://__token__:<your_personal_token>@gitlab.obspm.fr/api/v4/projects/2052/packages/pypi/simple --trusted-host gitlab.obspm.fr\n```\n\nYou will need a personal access token to reach the package registry in the ROC Gitlab server.\n\n### Installation from the repository\n\nFirst, retrieve the `FILM` repository from the ROC gitlab server:\n\n```\ngit clone https://gitlab.obspm.fr/ROC/Pipelines/Plugins/FILM.git\n```\n\nThen, install the package (here using (poetry)[https://python-poetry.org/]):\n\n```\npoetry install --extras "poppy plugin"\n```\n\nNOTES:\n\n    - It is also possible to clone the repository using SSH\n    - To install poetry: `pip install poetry`\n\n## Usage\n\nThe roc-film plugin is designed to be run in a POPPy-built pipeline.\nNevertheless, it is still possible to import some classes and methods in Python files.\n\n### How to release a new version of the plugin?\n\n1. Checkout to the git *develop* branch (and make pull to be sure to work from the latest commit in the gitlab server)\n\n2. First update metadata (version, dependencies, etc.) in the plugin *pyproject.toml* file.\n\n3. Then make sure the *descriptor.json* and *poetry.lock* files are also up-to-date.\n\nTo update the *descriptor.json* file, run the command:\n\n    python bump_descriptor.py -m <modification_message>\n\nTo update the *poetry.lock* file, enter:\n\n    poetry lock\n\nN.B. *poetry* Python package must be installed (see https://python-poetry.org/).\n\n4. Commit the changes in the *develop* branch. Make sure to commit with a comprehensive enough message.\n5. Checkout to the *master* branch and merge the *develop* branch into *master*\n6. Create a new git tag `X.Y.Z` for the new version of the plugin (must be the same version than in the *pyproject.toml* file)\n7. Push both the *master* branch and the tag to the gitlab server\n8. Do a rebase of *develop* onto the *master* branch\n9. Push the up-to-date *develop* branch to the gitlab server\n\nN.B. This procedure only concerns the version release. It is assumed that any other changes in the code have been already validated previously.\n\n## CONTACT\n\nxavier.bonnin@obspm.fr\nsonny.lion@obspm.fr\n',
    'author': 'Xavier Bonnin',
    'author_email': 'xavier.bonnin@obspm.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.obspm.fr/ROC/Pipelines/Plugins/FILM',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
