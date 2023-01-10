# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['searvey']

package_data = \
{'': ['*']}

install_requires = \
['Shapely',
 'beautifulsoup4',
 'erddapy',
 'geopandas',
 'html5lib',
 'limits',
 'lxml',
 'numpy',
 'pandas',
 'pydantic',
 'requests',
 'tqdm',
 'typepigeon',
 'xarray']

setup_kwargs = {
    'name': 'searvey',
    'version': '0.2.1',
    'description': '',
    'long_description': '# searvey\n\n[![pre-commit.ci](https://results.pre-commit.ci/badge/github/oceanmodeling/searvey/master.svg)](https://results.pre-commit.ci/latest/github/oceanmodeling/searvey/master)\n[![tests](https://github.com/oceanmodeling/searvey/actions/workflows/run_tests.yml/badge.svg)](https://github.com/oceanmodeling/searvey/actions/workflows/run_tests.yml)\n[![readthedocs](https://readthedocs.org/projects/pip/badge/)](https://readthedocs.org/projects/searvey)\n[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/oceanmodeling/searvey/master?urlpath=%2Flab)\n\nSearvey aims to provide the following functionality:\n\n- Unified catalogue of observational data including near real time.\n\n- Real time data analysis/clean up to facilitate comparison with numerical\n  models.\n\n- On demand data retrieval from multiple sources that currently include:\n\n    - U.S. Center for Operational Oceanographic Products and Services (CO-OPS)\n    - Flanders Marine Institute (VLIZ); Intergovernmental Oceanographic Commission (IOC)\n\n## Installation\n\nThe package can be installed with `conda`:\n\n`conda install -c conda-forge searvey`\n\n## Development\n\n```\npython3 -mvenv .venv\nsource .venv/bin/activate\npoetry install\npre-commit install\n```\n\nIf you wish to use jupyterlab to test searvey, then, assuming you have an\nexisting jupyterlab\ninstallation, you should be able to add a kernel to it with:\n\n```bash\npython -m ipykernel install --user --name searvey\n```\n',
    'author': 'Panos Mavrogiorgos',
    'author_email': 'pmav99@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/oceanmodeling/searvey.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
