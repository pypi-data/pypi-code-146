# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eargait',
 'eargait.base',
 'eargait.event_detection',
 'eargait.preprocessing',
 'eargait.spatial_params',
 'eargait.utils']

package_data = \
{'': ['*']}

install_requires = \
['fau-colors>=1.0.1,<2.0.0',
 'joblib>=1.2.0',
 'nilspodlib>=3.2.2,<4.0.0',
 'pandas>=1.5.2',
 'pyts>=0.11.0,<0.12.0',
 'scipy>=1,<2,!=1.6.0',
 'signialib>=1.2.0,<2.0.0',
 'tpcp>=0.12,<1.0.0']

setup_kwargs = {
    'name': 'eargait',
    'version': '1.1.0',
    'description': '*Eargait* provides a set of algorithms and functions to process IMU data recorded with ear-worn IMU sensors and to estimate characteristic gait parameters. ',
    'long_description': '[![PyPI](https://img.shields.io/pypi/v/eargait)](https://pypi.org/project/eargait/)\n[![Documentation Status](https://readthedocs.org/projects/eargait/badge/?version=latest)](https://eargait.readthedocs.io/en/latest/?badge=latest)\n[![Test and Lint](https://github.com/mad-lab-fau/eargait/actions/workflows/test-and-lint.yml/badge.svg?branch=main)](https://github.com/mad-lab-fau/eargait/actions/workflows/test-and-lint.yml)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/eargait)\n\n# EarGait - The Gait Analysis Package for Ear-Worn IMU Sensors !\n\n*EarGait* provides a set of algorithms and functions to process IMU data recorded with ear-worn IMU sensors and to \nestimate characteristic gait parameters. \n\n\n<center> <img src="./docs/_static/logo/WalkingHearingAid.png" height="200"/></center>\n\n\n## Getting started\n\n### Installation\n\nEasily install `eargait` via pip:\n```\npip install eargait\n```\n\nor add it to your project with [poetry](https://python-poetry.org/):\n```\npoetry add eargait\n```\n\n### Prerequisites\n*EarGait* only supports Python 3.8 and newer.\nFirst, install a compatible version of Python.\n\n### Help with setting up a virtual environment\nWe recommend installing the packages in a virtual environment (e.g. conda/Anaconda/miniconda).\nFor more information regarding Anaconda, please visit [Anaconda.com](https://docs.anaconda.com/anaconda/install/index.html). <br />\nIf you want to install the packages directly on the local python version, directly go to [Install Packages](#install-packages)  <br />\n\nIf you are familiar with virtual environments you can ``also use any other type of virtual environment. \nFurthermore, you can also directly install the python packages on the local python version, however, we would not recommend doing so.\n\n**In PyCharm** <br />\nSee [documentation](https://www.jetbrains.com/help/pycharm/conda-support-creating-conda-virtual-environment.html).\n\n**Shell/Terminal** <br /> \nFirst, verify that you have a working conda installation. Open a terminal/shell and type\n```\nconda env list\n```\nIf an error message similar to the one below is displayed, you probably do not have a working conda version installed. \n```\nconda: command not found\n```\nIn the shell/terminal:\n```\nconda create --no-default-packages -n gait_analysis python=3.8\n```\n*gait_analysis* is the name of the virtual environment. This environment can now also be included in PyCharm, \nas described See [here](https://www.jetbrains.com/help/pycharm/conda-support-creating-conda-virtual-environment.html) \nby using the existing environment option. <br /> \nTo check, whether the virtual environment has been created successfully, run again:\n```\nconda env list\n```\nThe environment *gait_analysis* should now be displayed.  <br /> \nActivate conda environment and install packages (see below).\n \n```\nconda activate gait_analysis\n```\n\nFor more help: [Conda Documentation](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)\n\n\n### Install Package in virtual environment\nIf you are using the conda environment, activate environment (in shell/terminal) (see above).\nUpdate pip and install `eargait`.\n```\npip install --upgrade pip \npip install eargait\n```\n\n## Check successful installation\n\nTo check whether the installation was successful, run the following line directly after installing `eargait` in the same shell/terminal: \n```\npython examples/check_installation/check_installation.py\n```\nShould return: `Installation was successful!`\n\n\n## Learn More\n[Documentation](https://eargait.readthedocs.io/en/latest/),\n[User Guide](https://eargait.readthedocs.io/en/latest/guides/index.html#user-guides),\n\n\n## Dev Setup\nWe are using poetry to manage dependencies and poethepoet to run and manage dev tasks. \n\nTo set up the dev environment including the required dependencies for using EarGait run the following commands:\n```\ngit clone https://github.com/mad-lab-fau/eargait\ncd eargait\npoetry install\n```\nAfterwards you can start to develop and change things. \nIf you want to run tests, format your code, build the docs, ..., \nyou can run one of the following poethepoet commands\n\n```\nCONFIGURED TASKS\n  format         \n  lint           Lint all files with Prospector.\n  check          Check all potential format and linting issues.\n  test           Run Pytest with coverage.\n  docs           Build the html docs using Sphinx.\n  bump_version   \n```\nby calling\n```\npoetry run poe <command name>\n```\n\n\n## Citing EarGait\n\nIf you use `Eargait` in your work, please report the version you used in the text. Additionally, please also cite the corresponding paper:\n\n```\nSeifer et al., (2022). TODO:, https://doi.org/TODO\n```\n\n\n## Acknowledgement\n\nEarGait is part of a research project from the Machine Learning and Data Analytics Lab, Friedrich-Alexander Universität Erlangen-Nürnberg. The authors thank WS Audiology, Erlangen, Germany and Lynge, Denmark for funding the work and their support which made this contribution possible.\n\n\n## Contribution\n\nThe entire development is managed via [GitHub](https://github.com/mad-lab-fau/eargait).\nIf you run into any issues, want to discuss certain decisions, want to contribute features or feature requests, just \nreach out to us by [opening a new issue](https://github.com/mad-lab-fau/eargait/issues/new/choose).\n\n',
    'author': 'Ann-Kristin Seifer',
    'author_email': 'ann-kristin.seifer@fau.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mad-lab-fau/eargait',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
