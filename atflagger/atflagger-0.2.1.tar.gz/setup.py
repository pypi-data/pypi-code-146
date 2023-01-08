# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['atflagger']
install_requires = \
['astropy>=5,<6',
 'bokeh',
 'dask>=2022,<2023',
 'distributed>=2022,<2023',
 'h5py',
 'matplotlib',
 'numpy',
 'tqdm',
 'xarray']

entry_points = \
{'console_scripts': ['atflagger = atflagger:cli']}

setup_kwargs = {
    'name': 'atflagger',
    'version': '0.2.1',
    'description': 'Simple method for flagging UWL data.',
    'long_description': '# atflagger\n\nA simple flagger for continuum UWL data. Flag persistent RFI first, then run this auto-flagger.\n\n## Installation\n\nInstalling requires `pip` and `python3` (3.8 and up).\n\nStable version:\n```\npip install atflagger\n```\n\nLatest version:\n```\npip install git+https://github.com/AlecThomson/atflagger\n```\n\n## Usage\n```\n❯ atflagger -h\nusage: atflagger [-h] [--beam BEAM] [--sigma SIGMA] [--n_windows N_WINDOWS] filenames [filenames ...]\n\nFlag SDHDF data\n\npositional arguments:\n  filenames             Input SDHDF file(s)\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --beam BEAM           Beam label\n  --sigma SIGMA         Sigma clipping threshold\n  --n_windows N_WINDOWS\n                        Number of windows to use in box filter\n```\n',
    'author': 'Alec Thomson',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
