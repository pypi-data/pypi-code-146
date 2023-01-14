# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openpack_toolkit',
 'openpack_toolkit.activity',
 'openpack_toolkit.bin',
 'openpack_toolkit.codalab',
 'openpack_toolkit.codalab.operation_segmentation',
 'openpack_toolkit.configs',
 'openpack_toolkit.configs.datasets',
 'openpack_toolkit.data',
 'openpack_toolkit.download',
 'openpack_toolkit.utils']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22.3,<2.0.0',
 'omegaconf>=2.2.2,<3.0.0',
 'pandas>=1.5.2,<2.0.0',
 'scikit-learn>=1.2.0,<2.0.0',
 'scipy>=1.7.3,<2.0.0']

entry_points = \
{'console_scripts': ['optk-download = '
                     'openpack_toolkit.bin.download:entry_func']}

setup_kwargs = {
    'name': 'openpack-toolkit',
    'version': '0.7.0',
    'description': 'Toolkit for OpenPack Dataset',
    'long_description': '# OpenPack Dataset Toolkit (optk)\n\n![OpenPack Dataset Logo](./img/OpenPackDataset-black.png)\n\n[![Test](https://github.com/open-pack/openpack-toolkit/actions/workflows/test.yaml/badge.svg)](https://github.com/open-pack/openpack-toolkit/actions/workflows/test.yaml)\n[![API Docs - GitHub Pages](https://github.com/open-pack/openpack-toolkit/actions/workflows/deploy-docs.yaml/badge.svg)](https://github.com/open-pack/openpack-toolkit/actions/workflows/deploy-docs.yaml)\n\n["OpenPack Dataset"](https://open-pack.github.io) is a new large-scale multi modal dataset of manual packing process.\nOpenPack is an open access logistics-dataset for human activity recognition, which contains human movement and package information from 16 distinct subjects.\nThis repository provide utilities to explore our exciting dataset.\n\n## Docs\n\n### Dataset\n\n- [Subjects & Recording Scenarios](./docs/USER.md)\n- [Activity Class Definition](./docs/ANNOTATION.md)\n- [Modality](./docs/DATA_STREAM.md)\n- [Data Split (Train/Val/Test/Submission)](./docs/DATA_SPLIT.md)\n\n### Task & Activity Recognition Challenge\n\n- Work Operation Recognition\n  - [OpenPack Challenge 2022](./docs/OPENPACK_CHALLENGE/)\n\n### Sample Data\n\n[Sample](./samples/)\n\n## Install\n\nWe provide some utility functions as python package. You can install via pip with the following command.\n\n```bash\n# Pip\npip install openpack-toolkit\n\n# Poetry\npoetry add  openpack-toolkit\n```\n\n## Examples\n\n### Tutorial\n\n- [Download and Visualization (Notebook)](./samples/OpenPack_DataVisualization.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/open-pack/openpack-toolkit/blob/main/samples/OpenPack_DataVisualization.ipynb)\n\n### Work Activity Recognition (PyTorch)\n\nPyTorch code samples for work operation prediction task is available.\nSee [openpack-torch](https://github.com/open-pack/openpack-torch) for more dietail.\n\n## Download Dataset\n\n```bash\noptk-download -d ../data/datasets\n\n# If you are a user of poetry,\npoetry run optk-download -d ../data/datasets\n```\n\nHelp:\n\n```txt\n$ poetry run optk-download -d ../data/datasets -h\nusage: optk-download [-h] -d DATASET_DIR [-v VERSION] [-s STREAMS]\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -d DATASET_DIR, --dataset-dir DATASET_DIR\n                        Path to dataset directory. Downloaded data will be stored under the directory\n  -v VERSION, --version VERSION\n                        Target dataset version. Default: v0.2.0\n  -s STREAMS, --streams STREAMS\n                        A list of data stream names that you want to download.\n                        Stream names must be separated by commas. If none, all\n                        data in zenodo will be downloaded. Defaul: none\n```\n\n\n## Links\n\n- [Homepage](https://open-pack.github.io/) (External Site)\n  - [OpenPack Challenge 2022](https://open-pack.github.io/challenge2022) (External Site)\n- [zenodo](https://doi.org/10.5281/zenodo.5909086)\n- [API Docs](https://open-pack.github.io/openpack-toolkit/openpack_toolkit/)\n- [PyPI](https://pypi.org/project/openpack-toolkit/)\n- [openpack-torch](https://github.com/open-pack/openpack-torch)\n\n![OpenPack Challenge Logo](./img/OpenPackCHALLENG-black.png)\n\n## License\n\nopenpack-toolkit has a MIT license, as found in the [LICENSE](./LICENCE) file.\n\nNOTE: [OpenPack Dataset](https://doi.org/10.5281/zenodo.5909086) itself is available under [Creative Commons Attribution Non Commercial Share Alike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode) license.\n',
    'author': 'Yoshimura Naoya',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://open-pack.github.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
