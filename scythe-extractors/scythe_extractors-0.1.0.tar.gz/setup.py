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
    'version': '0.1.0',
    'description': 'A library of tools that generate summaries of the data contained in scientific data files',
    'long_description': 'None',
    'author': 'Materials Data Facility',
    'author_email': 'materialsdatafacility@uchicago.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8.0,<3.11',
}


setup(**setup_kwargs)
