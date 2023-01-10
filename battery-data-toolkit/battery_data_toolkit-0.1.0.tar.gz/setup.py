# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['batdata',
 'batdata.extractors',
 'batdata.extractors.tests',
 'batdata.postprocess',
 'batdata.postprocess.tests',
 'batdata.schemas',
 'batdata.schemas.tests',
 'batdata.tests']

package_data = \
{'': ['*'], 'batdata.extractors.tests': ['files/*', 'files/batteryarchive/*']}

install_requires = \
['h5py>=3,<4',
 'pandas>1.0',
 'pydantic>=1.7,<2.0',
 'scipy>=1.3,<2.0',
 'scythe-extractors>=0.1,<0.2',
 'tables>=3.6,<4.0',
 'tqdm',
 'xlrd']

entry_points = \
{'console_scripts': ['batdata-convert = batdata.cli:main']}

setup_kwargs = {
    'name': 'battery-data-toolkit',
    'version': '0.1.0',
    'description': 'Utilities for reading and manipulating battery testing data',
    'long_description': '# Battery Data Extractor \n\n[![Python Package using Conda](https://github.com/materials-data-facility/battery-data-toolkit/actions/workflows/python-package-conda.yml/badge.svg)](https://github.com/materials-data-facility/battery-data-toolkit/actions/workflows/python-package-conda.yml)\n[![Coverage Status](https://coveralls.io/repos/github/materials-data-facility/battery-data-toolkit/badge.svg?branch=add-coverage)](https://coveralls.io/github/materials-data-facility/battery-data-toolkit?branch=master)\n\nThis directory contains utilities for converting battery testing data files from native formats\nto a standardized HDF5 file.\n\nIt also contains some scripts that run these utilities on datasets available to the ASOH project.\n\n## Installation\n\nThe package can be installed with pip,\nwhich will install the minimal amount of packages needed for this library\nto function:\n\n```bash\npip install -r requirements.txt\npip install -e .\n```\n\nFor development purposes, we recommend installing the library and \nall requirements\nusing Anaconda rather than pip. \nAnaconda reliably gathers compatible \nversions of all libraries and we have the versions of the libraries\nfixed in that development environment.\nInstall the environment using: \n\n`conda env create --file environment.yml --force`\n\n## Project Organization\n\nThe `scripts` folder holds code that processes different datasets used by our collaboration. \n\nAny logic that is general enough to warrant re-use is moved into the `batdata` Python package.\n\nThe Python package also holds the schemas, which are described in \n[`schemas.py`](./batdata/schemas/__init__.py).\n',
    'author': 'Logan Ward',
    'author_email': 'lward@anl.gov',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/materials-data-facility/battery-data-toolkit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
}


setup(**setup_kwargs)
