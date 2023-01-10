# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['roc',
 'roc.idb',
 'roc.idb.commands',
 'roc.idb.converters',
 'roc.idb.models',
 'roc.idb.models.music',
 'roc.idb.models.versions',
 'roc.idb.parsers',
 'roc.idb.parsers.mib_parser',
 'roc.idb.parsers.palisade_parser',
 'roc.idb.parsers.srdb_parser',
 'roc.idb.tasks',
 'roc.idb.tests',
 'roc.idb.tools']

package_data = \
{'': ['*']}

install_requires = \
['poppy-core>=0.9.4', 'poppy-pop>=0.7.5', 'sqlalchemy', 'xlwt==1.3.0']

setup_kwargs = {
    'name': 'roc-idb',
    'version': '1.4.3',
    'description': 'Plugin to manage the IDB',
    'long_description': '# ROC IDB\n\nA plugin to manage different IDB source/version for RPW/Solar Orbiter.\n\n## User guide\n\n### Pre-requisites\n\nThe following software must be installed:\n- Python 3.8\n- pip tool\n- poetry (optional)\n- git (optional)\n\n### Install a stable release with pip\n\nTo install the roc-idb plugin with pip:\n\n``pip install roc-idb``\n\n## Nominal usage\n\nroc-idb is designed to be called from a pipeline running with the POPPy framework.\n\nThe plugin can be used in Python programs using "import roc.idb".\n\n## Developer guide\n\n### Install a local copy from source files\n\nTo install a local copy of the roc-idb plugin:\n\n1. Retrieve a copy of the source files from https://gitlab.obspm.fr/ROC/Pipelines/Plugins/IDB (restricted access)\n2. Use `pip install` or `poetry install` command to install local instance\n\n### Publish a new tag on Gitlab\n\n1. Update the version using ``poetry version <bump_level>`` where <bump_level> can be patch, minor or major\n2. Update the descriptor using ``poetry run python bump_descriptor.py``\n3. Generate the new setup file using ``poetry run dephell deps convert``\n4. Apply code formatters using ``poetry run pre-commit run -a``\n5. Commit and tag\n\nAuthors\n-------\n\n* Xavier BONNIN xavier.bonnin@obspm.fr (maintainer)\n* Sonny LION sonny.lion@obspm.fr (author)\n\nLicense\n-------\n\nThis project is licensed under CeCILL-C.\n\nAcknowledgments\n---------------\n\n* Solar Orbiter / RPW Operation Centre (ROC) team\n',
    'author': 'Xavier BONNIN',
    'author_email': 'xavier.bonnin@obspm.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.obspm.fr/ROC/Pipelines/Plugins/IDB',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
