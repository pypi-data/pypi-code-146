# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['roc',
 'roc.dingo',
 'roc.dingo.models',
 'roc.dingo.models.versions',
 'roc.dingo.tasks',
 'roc.dingo.templates',
 'roc.dingo.tests',
 'roc.dingo.tests.test-1-tasks',
 'roc.dingo.tests.test-2-commands']

package_data = \
{'': ['*'],
 'roc.dingo.models.versions': ['SQL/*'],
 'roc.dingo.tests': ['data-tasks/*']}

install_requires = \
['SQLAlchemy>=1.3,<2.0',
 'alembic>=1.4,<2.0',
 'astropy>=5.2,<6.0',
 'numpy!=1.19.5',
 'pandas>=1.1.3',
 'poppy-core>=0.9.4',
 'poppy-pop>=0.7.5',
 'psycopg2>=2.8.4,<3.0.0',
 'roc-idb>=1.0,<2.0',
 'roc-rpl>=1.0,<2.0',
 'spacepy>=0.4.1,<0.5.0',
 'spice_manager>=1.1.0,<2.0.0',
 'xmltodict>=0.13,<0.14']

setup_kwargs = {
    'name': 'roc-dingo',
    'version': '1.3.7',
    'description': 'Data INgestOr (DINGO) plugin is used to ingest data into the ROC pipeline database',
    'long_description': 'DINGO PLUGIN README\n===================\n\n[![pipeline status](https://gitlab.obspm.fr/ROC/Pipelines/Plugins/DINGO/badges/develop/pipeline.svg)](https://gitlab.obspm.fr/ROC/Pipelines/Plugins/DINGO/pipelines)\n[![coverage report](https://gitlab.obspm.fr/ROC/Pipelines/Plugins/DINGO/badges/develop/coverage.svg)](https://roc.pages.obspm.fr/Pipelines/Plugins/DINGO/pytest_coverage_html/)\n[![tests status](https://roc.pages.obspm.fr/Pipelines/Plugins/DINGO/pie.svg)](https://roc.pages.obspm.fr/Pipelines/Plugins/DINGO/report.html)\n\nThis directory contains the source files of the Data INGestOr (DINGO), a plugin of the ROC pipeline used to ingest data into the ROC database.\nDINGO is developed with and run under the POPPY framework.\n\n## User guide\n\n### Pre-requisites\n\nThe following software must be installed:\n- Python 3.8\n- pip tool\n- poetry (optional)\n- git (optional)\n\n### Install a stable release with pip\n\nTo install the roc-dingo plugin with pip:\n\n``pip install roc-dingo``\n\n## Nominal usage\n\nroc-dingo is designed to be called from a pipeline running with the POPPy framework.\n\nThe plugin can be used in Python programs using "import roc.dingo".\n\n## Developer guide\n\n### Install a local copy from source files\n\nTo install a local copy of the roc-dingo plugin:\n\n1. Retrieve a copy of the source files from https://gitlab.obspm.fr/ROC/Pipelines/Plugins/DINGO (restricted access)\n2. Use `pip install` or `poetry install` command to install local instance\n\n### Publish a new version\n\n1. Update the plugin version in pyproject.toml\n2. Update the plugin descriptor using ``python bump_descriptor.py -m <message>``\n3. Update `poetry.lock` file running `poetry lock`\n4. Always commit in `develop` branch first\n5. Merge in `master/main` branch and tag the version\n\nN.B. When a new tag is pushed in gitlab, tests are automatically run in pipeline, then plugin published in pypi.\n\nAuthors\n-------\n\n* Florence HENRY florence.henry@obspm.fr (maintainer)\n* Xavier BONNIN xavier.bonnin@obspm.fr (maintainer)\n* Sonny LION sonny.lion@obspm.fr (author)\n\nLicense\n-------\n\nThis project is licensed under CeCILL-C.\n\nAcknowledgments\n---------------\n\n* Solar Orbiter / RPW Operation Centre (ROC) team\n',
    'author': 'Florence Henry',
    'author_email': 'florence.henry@obspm.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.obspm.fr/ROC/Pipelines/Plugins/DINGO',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
