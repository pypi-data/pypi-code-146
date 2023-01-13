# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['roc',
 'roc.guest',
 'roc.guest.models',
 'roc.guest.models.meb_gse',
 'roc.guest.models.meb_gse_data',
 'roc.guest.models.versions',
 'roc.guest.tasks',
 'roc.guest.tests']

package_data = \
{'': ['*'], 'roc.guest': ['scripts/*', 'templates/*']}

install_requires = \
['Jinja2>=3.0,<4.0',
 'mysqlclient>=1.4.6,<2.0.0',
 'poppy-core',
 'poppy-pop',
 'roc-film>=1.0,<2.0',
 'roc-rpl>=1.0,<2.0']

setup_kwargs = {
    'name': 'roc-guest',
    'version': '1.3.0',
    'description': 'Gse data ReqUESTer (GUEST): Plugin to handle data products from/to ground tests (MEB GSE, ADS GSE)',
    'long_description': 'GUEST PLUGIN README\n===================\n\nThe RPW Gse data ReqUESTer (GUEST) is a plugin used to handle data from GSE for RPW/Solar Orbiter (MEB GSE, ADS GSE).\n\nGUEST is designed to be run in an instance of the ROC Ground Test SGSE (RGTS).\n\nGUEST is developed with and run under the POPPY framework.\n\n## Quickstart\n\n### Installation with pip\n\nTo install the plugin using pip:\n\n```\npip install roc-guest\n```\n\n### Installation from the repository (restricted access)\n\nFirst, retrieve the `GUEST` repository from the ROC gitlab server:\n\n```\ngit clone https://gitlab.obspm.fr/ROC/Pipelines/Plugins/GUEST.git\n```\n\nThen, install the package (here using (poetry)[https://python-poetry.org/]):\n\n```\npoetry install"\n```\n\nNOTES:\n\n    - It is also possible to clone the repository using SSH\n    - To install poetry: `pip install poetry`\n\n## Usage\n\nThe roc-guest plugin is designed to be run in a POPPy-built pipeline.\nNevertheless, it is still possible to import some classes and methods in Python files.\n\n## CONTACT\n\n* roc dot support at sympa dot obspm dot fr\n\n## License\n\n\nThis project is licensed under CeCILL-C.\n\n## Acknowledgments\n\nSolar Orbiter / RPW Operation Centre (ROC) team\n',
    'author': 'Xavier Bonnin',
    'author_email': 'xavier.bonnin@obspm.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.obspm.fr/ROC/Pipelines/Plugins/GUEST',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
