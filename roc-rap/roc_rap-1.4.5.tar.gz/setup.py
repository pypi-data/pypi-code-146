# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['roc',
 'roc.rap',
 'roc.rap.config',
 'roc.rap.tasks',
 'roc.rap.tasks.bia',
 'roc.rap.tasks.lfr',
 'roc.rap.tasks.lfr.bp',
 'roc.rap.tasks.tds',
 'roc.rap.tasks.thr',
 'roc.rap.tests',
 'roc.rap.tools']

package_data = \
{'': ['*']}

install_requires = \
['Cython>=0.29,<0.30',
 'h5py>=3.7,<4.0',
 'numpy!=1.19.5',
 'pandas>=1.1.3',
 'poppy-core',
 'poppy-pop',
 'roc-dingo>=1.0,<2.0',
 'roc-idb>=1.0,<2.0',
 'roc-rpl>=1.0,<2.0',
 'spice_manager']

setup_kwargs = {
    'name': 'roc-rap',
    'version': '1.4.5',
    'description': 'Rpw dAta Processor (RAP): a plugin used to process RPW L0, L1 and HK data',
    'long_description': 'RAP PLUGIN README\n=================\n\n[![pipeline status](https://gitlab.obspm.fr/ROC/Pipelines/Plugins/RAP/badges/develop/pipeline.svg)](https://gitlab.obspm.fr/ROC/Pipelines/Plugins/RAP/pipelines)\n\nThis directory contains the source files of the Rpw dAta Processor (RAP), a plugin of the ROC pipelines dedicated to process RPW L0 data into L1.\n\nRAP has been developed with the [POPPY framework](https://poppy-framework.readthedocs.io/en/latest/).\n\n## Quickstart\n\n### Installation with pip\n\nTo install the plugin using pip:\n\n```\npip install roc-rap\n```\n\nNOTES:\n\n    - It is also possible to install roc-rap from gitlab using the command `pip install roc-rap --extra-index-url https://__token__:<your_personal_token>@gitlab.obspm.fr/api/v4/projects/2052/packages/pypi/simple --trusted-host gitlab.obspm.fr`. A personnal access token is required to reach the package registry in the ROC Gitlab server.\n\n### Installation from the repository\n\nFirst, retrieve the `RAP` repository from the ROC gitlab server:\n\n```\ngit clone https://gitlab.obspm.fr/ROC/Pipelines/Plugins/RAP.git\n```\n\nThen, install the package (here using (poetry)[https://python-poetry.org/]):\n\n```\npoetry install\n```\n\nNOTES:\n\n    - It is also possible to clone the repository using SSH\n    - To install poetry: `pip install poetry`\n    - Default branch is `develop`\n\n## Usage\n\nThe roc-rap plugin is designed to be run in a POPPy-built pipeline.\nNevertheless, it is still possible to import some classes and methods in Python files.\n\n## Contacts\n\n- xavier.bonnin@obspm.fr\n',
    'author': 'Xavier Bonnin',
    'author_email': 'xavier.bonnin@obspm.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.obspm.fr/ROC/Pipelines/Plugins/RAP',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
