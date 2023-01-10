# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['roc',
 'roc.rpl',
 'roc.rpl.compressed',
 'roc.rpl.packet_parser',
 'roc.rpl.packet_parser.parser',
 'roc.rpl.packet_structure',
 'roc.rpl.rice',
 'roc.rpl.tasks',
 'roc.rpl.tests',
 'roc.rpl.time']

package_data = \
{'': ['*'], 'roc.rpl.tests': ['data/*']}

install_requires = \
['Cython>=0.29,<0.30',
 'maser-tools',
 'numpy!=1.19.5',
 'poppy-core>=0.9.4',
 'poppy-pop>=0.7.5',
 'roc-idb>=1.0,<2.0',
 'spice_manager']

setup_kwargs = {
    'name': 'roc-rpl',
    'version': '1.5.1',
    'description': 'RPW Packet parsing Library (RPL): a plugin for the RPW TM/TC packet analysis',
    'long_description': 'RPL PLUGIN README\n=================\n\n[![pipeline status](https://gitlab.obspm.fr/ROC/Pipelines/Plugins/RPL/badges/develop/pipeline.svg)](https://gitlab.obspm.fr/ROC/Pipelines/Plugins/RPL/pipelines)\n\nThis directory contains the source files of the RPW Packet parsing Library (RPL), a plugin of the ROC pipelines dedicated to parse the RPW telemetry/command packets.\n\nRPL has been developed with the [POPPY framework](https://poppy-framework.readthedocs.io/en/latest/).\n\n## Quickstart\n\n### Installation with pip\n\nTo install the plugin using pip:\n\n```\npip install roc-rpl\n```\n\nNOTES:\n\n    - It is also possible to install plugin from gitlab: `pip install roc-rpl --extra-index-url https://__token__:<your_personal_token>@gitlab.obspm.fr/api/v4/projects/2052/packages/pypi/simple --trusted-host gitlab.obspm.fr`. A personal access token is required to reach the package registry in the ROC Gitlab server.\n\n### Installation from the repository\n\nFirst, retrieve the `RPL` repository from the ROC gitlab server:\n\n```\ngit clone https://gitlab.obspm.fr/ROC/Pipelines/Plugins/RPL.git\n```\n\nThen, install the package (here using (poetry)[https://python-poetry.org/]):\n\n```\npoetry install --extras "poppy"\n```\n\nNOTES:\n\n    - It is also possible to clone the repositiory using SSH\n    - To install poetry: `pip install poetry`\n    - Default branch is `develop`\n\n## Usage\n\nThe roc-rpl plugin is designed to be run in a POPPy-built pipeline.\nNevertheless, it is still possible to import some classes and methods in Python files.\n\nFor instance, to test that the installation has ended correctly, run:\n\n```\npython -c "from roc.rpl import packet_structure"\n```\n\nNo message should be returned if the import works well.\n\n## Authors\n\n* Xavier BONNIN xavier.bonnin@obspm.fr (maintainer)\n* Manuel DUARTE manuel.duarte@obspm.fr (author)\n* Sonny LION sonny.lion@obspm.fr (author)\n\nLicense\n-------\n\nThis project is licensed under CeCILL-C.\n\nAcknowledgments\n---------------\n\n* Solar Orbiter / RPW Operation Centre (ROC) team\n',
    'author': 'Xavier Bonnin',
    'author_email': 'xavier.bonnin@obspm.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.obspm.fr/ROC/Pipelines/Plugins/RPL',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
