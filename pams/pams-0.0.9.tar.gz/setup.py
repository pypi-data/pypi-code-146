# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pams',
 'pams.agents',
 'pams.events',
 'pams.logs',
 'pams.runners',
 'pams.utils']

package_data = \
{'': ['*']}

install_requires = \
['tqdm>=4.64.1,<5.0.0']

extras_require = \
{':python_version >= "3.7" and python_version < "3.8"': ['numpy>=1.21.0,<2.0.0',
                                                         'scipy>=1.7.0,<2.0.0'],
 ':python_version >= "3.8" and python_version < "4.0"': ['numpy>=1.23.4,<2.0.0',
                                                         'scipy>=1.9.2,<2.0.0']}

setup_kwargs = {
    'name': 'pams',
    'version': '0.0.9',
    'description': 'PAMS: Platform for Artificial Market Simulations',
    'long_description': '# pams\nPAMS: Platform for Artificial Market Simulations\n\n[![python](https://img.shields.io/pypi/pyversions/pams.svg)](https://pypi.org/project/pams)\n[![pypi](https://img.shields.io/pypi/v/pams.svg)](https://pypi.org/project/pams)\n[![CI](https://github.com/masanorihirano/pams/actions/workflows/ci-python.yml/badge.svg)](https://github.com/masanorihirano/pams/actions/workflows/ci-python.yml)\n[![downloads](https://img.shields.io/pypi/dm/pams)](https://pypi.org/project/pams)\n[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Codacy Badge](https://app.codacy.com/project/badge/Grade/18ed1eecc4f34a99bb6fd9a7160f78ca)](https://www.codacy.com/gh/masanorihirano/pams/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=masanorihirano/pams&amp;utm_campaign=Badge_Grade)\n[![codecov](https://codecov.io/gh/masanorihirano/pams/branch/main/graph/badge.svg?token=tFccElw7Wd)](https://codecov.io/gh/masanorihirano/pams)\n\n## Documentations & User Guides\n\nDocumentations are available on [readthedoc](https://pams.hirano.dev/)\n\n## Install\nThis package is available on pypi as [`pams`](https://pypi.org/project/pams/)\n```bash\n$ pip install pams\n$ python\n>> import pams\n```\n\n## Citation\nCurrently, no publication related to this repository. Therefore, please cite this repository directly if you want.\n```bibtex\n@misc{Hirano2022-pams\n    title={{PAMS: Platform for Artificial Market Simulations}},\n    autors={Masanori HIRANO, Ryosuke TAKATA},\n    year={2022},\n    url = {https://github.com/masanorihirano/pams}\n}\n```\n\n## Issues and Contribution\nAbout issues (bugs):\n-   You can report issues [here](https://github.com/masanorihirano/pams/issues).\n-   There are no guarantee to support or fix those issues.\n\nContributions:\n-   You can send pull requests (PRs) to this repository.\n-   But, there are no guarantee to merge your PRs.\n\n',
    'author': 'Masanori HIRANO',
    'author_email': 'masa.hirano.1996@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
