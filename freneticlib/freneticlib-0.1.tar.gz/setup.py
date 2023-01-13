# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['freneticlib',
 'freneticlib.core',
 'freneticlib.core.mutation',
 'freneticlib.executors',
 'freneticlib.executors.beamng',
 'freneticlib.executors.bicycle',
 'freneticlib.executors.bicycle.agents.tools',
 'freneticlib.representations',
 'freneticlib.stopcriteria',
 'freneticlib.utils']

package_data = \
{'': ['*'], 'freneticlib.executors': ['autonomoose/*']}

install_requires = \
['beamngpy',
 'bezier',
 'click',
 'matplotlib',
 'numpy',
 'pandas',
 'scipy',
 'shapely']

extras_require = \
{'test': ['pytest']}

setup_kwargs = {
    'name': 'freneticlib',
    'version': '0.1',
    'description': 'The Frenetic algorithm for search-based ADS road generation',
    'long_description': '# frenetic-lib\n\n## The Frenetic story\nFrenetic is a search-based algorithm, originally developed as submission to the\n[SBST 2021 Tool Competition](https://sbst21.github.io/program/).\nFrenetic was very successful and turned out to be one of the best tools that year.\n\nAfter the competition, we continued our development of Frenetic and adapted it\nfor various projects, including research on different road representations.\nWe noticed however, that the SBST tool pipeline (i.e. the execution flow) is geared specifically towards the competition and limits research versatility.\nHence, it was difficult to integrate a different driving agent or alter the execution routine.\n\nFurthermore, in the 2022 iteration of the SBST competition, we also observed that several competitors built upon Frenetic and its road representation.\nDue to its popularity, we decided to extract the "Frenetic-part" of our submission into a standalone library,\nso it can be more easily developed, maintained and integrated in other projects.\n\nAs a result, we extract Frenetic into this own library. This will support our own research\nand allow other people to more easily reuse the code.\n\n### Main features\nfrenetic helps you to\n- select a road representation (e.g. Bezier, Cartesian, Kappa, Theta),\n- define an objective (i.e. road feature to minimise/maximise),\n- choose mutation parameters,\n- define an executor (i.e. target executor), and\n- trigger execution (for a certain time/number of iterations)\n\nBehind the scenes, frenetic will take care of creating random roads (in your specified representation),\nfollowed by a mutation phase with the goal of producing a variety of individual roads\naccording to the chosen objective.\n\n\n### Where will the Frenetic journey go?\n\nIn the future, we want to ...\n\n# How to use\n\nFrenetic\'s main modules are the `Frenetic` and `FreneticCore` classes.\n`Frenetic` is responsible for the execution flow.\n\n\n, `FreneticCore`\n\n## Reference\nFor academic publications, please consider the following reference:\n\nE. Castellano, A. Cetinkaya, C. Ho Thanh, Stefan Klikovits, X. Zhang and P. Arcaini. Frenetic at the SBST 2021 Tool Competition. In: Proc. 2021 IEEE/ACM 14th International Workshop on Search-Based Software Testing (SBST). IEEE, 2021.\n```bibtex\n@InProceedings{Castellano:2021:SBST,\n  author={Castellano, Ezequiel and Cetinkaya, Ahmet and Thanh, Cédric Ho and Klikovits, Stefan and Zhang, Xiaoyi and Arcaini, Paolo},\n  title={Frenetic at the SBST 2021 Tool Competition},\n  booktitle={2021 IEEE/ACM 14th International Workshop on Search-Based Software Testing (SBST)},\n  year={2021},\n  editor={Jie Zhang and Erik Fredericks},\n  pages={36-37},\n  publisher={IEEE},\n  keywords={genetic algorithms, genetic programming},\n  doi={10.1109/SBST52555.2021.00016}\n}\n```\n\n# Contribute\nWe are warmly welcoming contributions in various forms.\nIf you find a bug or want to share an improvement, please don\'t hesitate to open a new issue.\n\nPlease also let us know if you used frenetic in your project.\nIt always feels good to know a project is used elsewhere.\n',
    'author': 'Stefan Klikovits',
    'author_email': 'stefan@klikovits.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ERATOMMSD/frenetic',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
