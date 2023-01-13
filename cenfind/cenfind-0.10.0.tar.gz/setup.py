# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cenfind',
 'cenfind.cli',
 'cenfind.core',
 'cenfind.experiments',
 'cenfind.labelbox']

package_data = \
{'': ['*']}

install_requires = \
['csbdeep>=0.6.3,<0.7.0',
 'imageio>=2.16.0,<3.0.0',
 'numpy>=1.21.2,<1.22',
 'opencv-python>=4.5.5.62,<5.0.0.0',
 'pandas>=1.4.1,<2.0.0',
 'pytomlpp>=1.0.10,<2.0.0',
 'scikit-image>=0.19.2,<0.20.0',
 'scikit-learn>=1.1.3,<2.0.0',
 'scipy>=1.7.1,<2.0.0',
 'spotipy-detector>=0.1.0,<0.2.0',
 'stardist>=0.8.3,<0.9.0',
 'tensorflow>=2.11.0,<3.0.0',
 'tifffile>=2022.5.4,<2023.0.0',
 'tqdm>=4.62.3,<5.0.0',
 'xarray>=0.21.1,<0.22.0']

entry_points = \
{'console_scripts': ['evaluate = cenfind.cli.evaluate:main',
                     'prepare = cenfind.cli.prepare:main',
                     'score = cenfind.cli.score:main',
                     'squash = cenfind.cli.squash:main',
                     'upload = cenfind.labelbox.upload_labels:main',
                     'vignettes = cenfind.labelbox.vignettes:main']}

setup_kwargs = {
    'name': 'cenfind',
    'version': '0.10.0',
    'description': 'Score cells for centrioles in IF data',
    'long_description': "# CenFind\n\nA command line interface to score cells for centrioles.\n\n## Introduction\n\n`cenfind` is a command line interface to detect and assign centrioles in immunofluorescence images of human cells. Specifically, it orchestrates:\n\n- the z-max projection of the raw files;\n- the detection of centrioles;\n- the detection of the nuclei;\n- the assignment of the centrioles to the nearest nucleus.\n\n## Installation\n1. Install python via pyenv\n2. Download and set up 3.9.5 as local version\n3. Set up Python interpreter\n```shell\npyenv local 3.9.5\npyenv global 3.9.5\n```\n4. Create a virtual environment for CenFind\n```shell\npython -m venv venv-cenfind\nsource venv-cenfind/bin/activate\n```\n\n5. Check that `cenfind`'s programs are correctly installed by running:\n\n```shell\nsquash --help\n```\n\n## Basic usage\nBefore scoring the cells, you need to prepare the dataset folder. \n`cenfind` assumes a fixed folder structure. \nIn the following we will assume that the .ome.tif files are all immediately in raw/. \nEach field of view is a z-stack containing 4 channels (0, 1, 2, 3). The channel 0 contains the nuclei and the channels 1-3 contains centriolar markers.\n\n```text\n<project_name>/\n└── raw/\n```\n2. Run `prepare` to initialise the folder with a list of fields and output folders:\n```shell\nprepare /path/to/dataset <list channels of centrioles, like 1 2 3, (if 0 is the nucleus channel)>\n```\n\n2. Run `squash` with the argument of the path to the project folder and the suffix of the raw files. `projections/` is populated with the max-projections `*_max.tif` files.\n```shell\nsquash path/to/dataset\n```\n\n3. Run `score` with the arguments source, the index of the nuclei channel (usually 0 or 3), the channel to score and the path to the model. You need to download it from https://figshare.com/articles/software/Cenfind_model_weights/21724421\n```shell\nscore /path/to/dataset /path/to/model/ 0 1 2 3 --projection_suffix '_max'\n```\n\nFor reference:\n```shell\nscore -h\nCENFIND: Automatic centriole scoring\n\npositional arguments:\n  path                  Path to the dataset\n  model                 Absolute path to the model folder\n  channel_nuclei        Channel index for nuclei segmentation, e.g., 0 or 3\n  channels              Channel indices to analyse, e.g., 1 2 3\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --vicinity VICINITY   Distance threshold in micrometer (default: -5 um)\n  --factor FACTOR       Factor to use: given a 2048x2048 image, 256 if 63x; 2048 if 20x:\n  --projection_suffix PROJECTION_SUFFIX\n                        Projection suffix (`_max` (default) or `_Projected`\n```\n\n4. Check that the predictions are satisfactory by looking at the folders `visualisation/` and `statistics/`\n\n## API\n\n`cenfind` consists of two core classes: `Dataset` and `Field`.\n\nA `Dataset` represents a collection of related fields, i.e., same pixel size, same channels, same cell type.\n\nIt should:\n- return the name\n- iterate over the fields,\n- construct the file name for the projections and the z-stacks\n- read the fields.txt\n- write the fields.txt file\n- set up the folders projections, predictions, visualisations and statistics\n- set and get the splits\n\nA `Field` represents a field of view and should:\n\n- construct file names for projections, annotation\n- get Dataset\n- load the projection as np.ndarray\n- load the channel as np.ndarray\n- load annotation as np.ndarray\n- load mask as np.ndarray\n\nUsing those two objects, `cenfind` should\n\n- detect centrioles (data, model) => points,\n- extract nuclei (data, model) => contours,\n- assign centrioles to nuclei (contours, points) => pairs\n- outline centrioles and nuclei (data, points) => image\n- create composite vignettes (data) => composite_image\n- flag partial nuclei (contours, tolerance) => contours\n- compare predictions with annotation (points, points) => metrics_namespace\n",
    'author': 'Leo Burgy',
    'author_email': 'leo.burgy@epfl.ch',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/UPGON/cenfind',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
