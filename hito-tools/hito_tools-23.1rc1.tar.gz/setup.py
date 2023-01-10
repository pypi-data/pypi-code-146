# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hito_tools']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.5,<2.0', 'requests>=2.28,<3.0']

setup_kwargs = {
    'name': 'hito-tools',
    'version': '23.1rc1',
    'description': 'Modules for interacting with Hito and NSIP',
    'long_description': "# hito_tools module\n\nCe repository contient le module Pyhton `hito_tools` utilisé par les autres outils Python autour de Hito (OSITAH, hito2lists...).\n\n\n## Installation\n\n### Environnement Python\n\nL'installation de [hito_tools](https://pypi.org/project/hito-tools) nécessite un environnement Python avec une version >= 3.8.\nIl est conseillé d'utiliser un environnement\nvirtuel pour chaque groupe d'applications et de déployer le module `hito_tools` dans cet environnemnt. Il est recommandé d'utiliser\nune distribution de Python totalement indépendante du système d'exploitation comme [pyenv](https://github.com/pyenv/pyenv),\n[poetry](https://python-poetry.org) ou [Anaconda](https://www.anaconda.com/products/individual). Pour la création d'un\nenvironnement virtuel avec Conda, voir la \n[documentation spécifique](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands).\n\nLes modules Python requis par ce module sont :\n* pandas (conda-forge)\n* requests (conda-forge)\n\nAvec `conda`, il faut utiliser l'option `-c conda-forge` lors de la commande `conda install`. \n\n\n### Installation du module hito_tools\n\nL'installation se fait avec la commande `pip` de l'environnement Python utilisé :\n\n```bash\npip install hito_tools\n```\n",
    'author': 'Michel Jouvin',
    'author_email': 'michel.jouvin@ijclab.in2p3.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
