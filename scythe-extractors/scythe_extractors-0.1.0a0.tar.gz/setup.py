# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scythe', 'scythe.adapters', 'scythe.utils']

package_data = \
{'': ['*'], 'scythe': ['schemas/*']}

install_requires = \
['llvmlite>=0.38.0,<0.39.0',
 'mdf-toolbox>=0.5.3,<0.6.0',
 'numba>=0.55,<0.56',
 'pandas>=1.4.2,<2.0.0',
 'stevedore>=3.5.0,<4.0.0']

extras_require = \
{'all': ['ase>=3.19,<3.20',
         'pymatgen>=2022.3.24,<2023.0.0',
         'tableschema>=1,<2',
         'dfttopif>=1.1.0,<2.0.0',
         'hyperspy>=1.4.1,<2.0.0',
         'python-magic>=0.4.15,<0.5.0',
         'Pillow>=9.0.1,<10.0.0',
         'xmltodict>=0.12.0,<0.13.0',
         'pycalphad>=0.10.0,<0.11.0'],
 'ase': ['ase>=3.19,<3.20'],
 'crystal-structure': ['ase>=3.19,<3.20', 'pymatgen>=2022.3.24,<2023.0.0'],
 'csv': ['tableschema>=1,<2'],
 'dft': ['dfttopif>=1.1.0,<2.0.0'],
 'electron-microscopy': ['hyperspy>=1.4.1,<2.0.0'],
 'file': ['python-magic>=0.4.15,<0.5.0'],
 'image': ['Pillow>=9.0.1,<10.0.0'],
 'tdb': ['pycalphad>=0.10.0,<0.11.0'],
 'xml': ['xmltodict>=0.12.0,<0.13.0']}

entry_points = \
{'scythe.adapter': ['greedy_serialize = '
                    'scythe.adapters.base:GreedySerializeAdapter',
                    'noop = scythe.adapters.base:NOOPAdapter',
                    'serialize = scythe.adapters.base:SerializeAdapter'],
 'scythe.extractor': ['ase = scythe.ase:ASEExtractor',
                      'crystal = '
                      'scythe.crystal_structure:CrystalStructureExtractor',
                      'csv = scythe.csv:CSVExtractor',
                      'dft = scythe.dft:DFTExtractor',
                      'em = '
                      'scythe.electron_microscopy:ElectronMicroscopyExtractor',
                      'filename = scythe.filename:FilenameExtractor',
                      'generic = scythe.file:GenericFileExtractor',
                      'image = scythe.image:ImageExtractor',
                      'json = scythe.json:JSONExtractor',
                      'noop = scythe.testing:NOOPExtractor',
                      'tdb = scythe.tdb:TDBExtractor',
                      'xml = scythe.xml:XMLExtractor',
                      'yaml = scythe.yaml:YAMLExtractor']}

setup_kwargs = {
    'name': 'scythe-extractors',
    'version': '0.1.0a0',
    'description': 'A library of tools that generate summaries of the data contained in scientific data files',
    'long_description': '# Scythe\n\n[![Build Status](https://github.com/materials-data-facility/Scythe/workflows/Build%20Status/badge.svg)](https://github.com/materials-data-facility/Scythe/actions/workflows/test-suite-and-docs.yml)\n[![Documentation](https://img.shields.io/badge/-Documentation-blue?style=flat&logo=bookstack&labelColor=grey&logoColor=white)](https://materials-data-facility.github.io/Scythe)\n[![Coverage Status](https://codecov.io/gh/materials-data-facility/Scythe/branch/master/graph/badge.svg)](https://codecov.io/gh/materials-data-facility/Scythe)\n[![GitHub last commit](https://img.shields.io/github/last-commit/materials-data-facility/Scythe)](https://github.com/materials-data-facility/Scythe/commits/master)\n[![PyPI version](https://badge.fury.io/py/scythe-extractors.svg)](https://badge.fury.io/py/scythe-extractors)\n[![GitHub contributors](https://img.shields.io/github/contributors/materials-data-facility/Scythe)](https://github.com/materials-data-facility/Scythe/graphs/contributors)\n\nScythe is a library of tools that generate summaries of the data contained in scientific data files.\nThe goal of Scythe is to provide a shared resources of these tools ("extractors") to avoid duplication of effort between the many emerging materials databases.\nEach extractor is designed to generate the sum of all data needed by each of these databases with a uniform API so that specific projects can write simple adaptors for their needs.\n\n## Installation\n\nInstall using an up-to-date version of `pip` on version 3.8 or higher of Python:\n\n```bash\npip install scythe-extractors\n```\n\nEach specific extractor module has its own set of required libraries.\nGiven that some modules have extensive dependencies, we do not install all of them automatically.\nYou can install them either module-by-module using the pip "extras" installation (e.g., \n`pip install scythe-extractors[image]"`),\nor install all extractors with \n`pip install scythe-extractors[all]"`.\n\n## Development/Contribution\n\nIf you wish to develop new features using Scythe, please consult the \n[Contributor Guide](https://materialsio.readthedocs.io/en/latest/contributor-guide.html) that will\nwalk you through installing [Poetry](https://python-poetry.org/) and the Scythe dependencies.\n\n## Documentation\n\n* Complete documentation for Scythe is on [Read the Docs](https://materialsio.readthedocs.io/en/latest/).\n* [List of Available Extractors](https://materialsio.readthedocs.io/en/latest/extractors.html)\n\n## Support \n\nThis work was performed in partnership with [Citrine Informatics](https://citrine.io/). \nThis was also performed under financial assistance award 70NANB14H012 from U.S. Department of Commerce, National Institute of Standards and Technology as part of the Center for Hierarchical Material Design (CHiMaD).\nThis work was also supported by the National Science Foundation as part of the Midwest Big Data Hub under NSF Award Number: 1636950 "BD Spokes: SPOKE: MIDWEST: Collaborative: Integrative Materials Design (IMaD): Leverage, Innovate, and Disseminate".\n',
    'author': 'Materials Data Facility',
    'author_email': 'materialsdatafacility@uchicago.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/materials-data-facility/scythe',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8.0,<3.11',
}


setup(**setup_kwargs)
