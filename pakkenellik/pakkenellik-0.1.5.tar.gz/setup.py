# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pakkenellik',
 'pakkenellik.aws',
 'pakkenellik.config',
 'pakkenellik.dataframe',
 'pakkenellik.datawrapper',
 'pakkenellik.google',
 'pakkenellik.integration',
 'pakkenellik.log',
 'pakkenellik.vegvesen',
 'pakkenellik.viz']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.26.39,<2.0.0',
 'bump2version>=1.0.1,<2.0.0',
 'geopandas>=0.12.2,<0.13.0',
 'gspread-dataframe>=3.3.0,<4.0.0',
 'gspread-formatting>=1.1.2,<2.0.0',
 'gspread>=5.7.2,<6.0.0',
 'pandas>=1.5.2,<2.0.0',
 'plotly>=5.11.0,<6.0.0',
 'pyjstat>=2.3.0,<3.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'pakkenellik',
    'version': '0.1.5',
    'description': "Swiss army knife for Bord4's data anlysis",
    'long_description': '# Pakkenellik: Bord4\'s swiss army knife for python projects\n\n<!-- TABLE OF CONTENTS -->\n<details open="open">\n  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>\n  <ol>\n    <li>\n      <a href="#about-the-project">About The Project</a>\n      <ul>\n        <li><a href="#requirements">Requirements</a></li>\n        <li><a href="#structure">Structure</a></li>\n      </ul>\n    </li>\n    <li>\n      <a href="#getting-started">Getting Started</a>\n      <ul>\n        <li><a href="#prerequisites">Prerequisites</a></li>\n        <li><a href="#installation">Installation</a></li>\n      </ul>\n    </li>\n    <li><a href="#usage">Usage</a></li>\n    <li><a href="#contributing">Contributing</a></li>\n    <li><a href="#contact">Contact</a></li>\n  </ol>\n</details>\n\n<!-- ABOUT THE PROJECT -->\n\n## About The Project\n\nPakkenellik is german and used in Bergen as a synonym for small packages one carry around, especially when traveling. This package is a swiss army knife for Bord4\'s python projects. It contains a makefile with commands for linting and formatting. One day it will contain testing as well.\n\nThis package is used by the [cookiecutter-bord4-analysis](https://github.com/BergensTidende/cookiecutter-bord4-analysis) project and [bord4-analysis-templates](https://github.com/BergensTidende/bord4-analysis-templates)\n\nInspiration for the makefile and potery-file is taken from Johannes Schmidt\'s series ["Setting up Python Projects"](https://johschmidt42.medium.com/setting-up-python-projects-part-i-408603868c08)\n\n\n## Installation\n\nRequires Python 3.10 or later.\n\n```bash\n\npip install pakkenellik\n\n```\n\nor using pipenv:\n\n```bash\n\npipenv install pakkenellik\n\n```\n\nor using poetry:\n\n```bash\npoetry add pakkenellik\n```\n\n## Usage\n\nThere are a heap of functions for you to use. Enjoy.\n\n## Local development\n\n### Requirements\n---\n\n- pyenv - manage python versions\n- poetry - manage python dependencies\n\nTo install on mac you can use homebrew:\n\n```bash\nbrew upgrade\nbrew install pyenv\n```\n\nYou can either install poetry with homebrew or the way described in the [documentation](https://python-poetry.org/docs/#installation)\n\n\n### Makefile commands\n\n- `make lint`\n  - lint the code in the src folder with black, isort and flake8. Mypy will check for correct typing.\n- `make format`\n  - format the code in the src folder with black and isort.\n\n### Structure\n\n```\n.\n├── .editorconfig\n├── .flake8\n├── pyproject.toml\n├── README.md\n└── pakkenellik\n    ├── __init__.py\n    ├── aws\n    │   ├── __init__.py\n    │   └── s3.py\n    ├── config\n    │   └── __init__.py\n    ├── dataframe\n    │   ├── __init__.py\n    │   ├── clean_column_headers.py\n    │   ├── datetime.py\n    │   ├── numbers.py\n    │   └── regions.py\n    ├── integration\n    │   ├── __init__.py\n    │   └── client.py\n    ├── log\n    │   ├── __init__.py\n    │   └── ansi.py\n    ├── vegvesen\n    │   ├── __init__.py\n    │   └── visvegen.py\n    └── viz\n        ├── __init__.py\n        └── pyplot.py\n```\n\n- `.editorconfig`\n  - Configuration file for editorconfig.\n- `.flake8`\n  - Configuration file for flake8.\n- `pyproject.toml`\n  - Configuration file for poetry. Mypy and isort is configured here.\n- `README.md`\n  - This file.\n- `pakkenellik`\n  - The package. It has the following subpackages:\n- `aws`\n  - util functions for working with AWS\n- `config`\n  - configuration functions that helps with adhering to bord4\'s folder structure and help with common urls. \n- `dataframe`\n  - util functions for working with dataframes\n- `integration`\n  - helper functions when working with Schibsted MM API\n- `log`\n  - better log functions\n- `vegvesen`\n  - Functions to work with Vegvesenet\'s VisVegen API\n\n## Usage\n\nTo install the package in your project run\n\n```bash\n\npoetry add pakkenellik\n```\n\n## Contributing\n\nDo you have write permissions to the repo? Then you can clone this project to a folder on your computer.\n\n```bash\ngit clone https://github.com/BergensTidende/pakkenellik.git\n```\n\nIf not do the following:\n\n- Create a personal fork of the project on Github.\n- Clone the fork on your local machine. Your remote repo on Github is called `origin`.\n- Add the original repository as a remote called `upstream`.\n- If you created your fork a while ago be sure to pull upstream changes into your local repository.\n\nThis will clone the repo into `pakkenellik`. \n\nCreate a branch for your changes\n\n```bash\ngit checkout -b name-of-branch\n```\n\nMake your changes, rememeber to commit. And always write your commit messages in the present tense. Your commit message should describe what the commit, when applied, does to the code – not what you did to the code.\n\nIf you\'re working on a clone push the branch to github and make PR.\n\nIf your\'re working a fork:\n\n- Squash your commits into a single commit with git\'s [interactive rebase](https://help.github.com/articles/interactive-rebase). Create a new branch if necessary.\n- Push your branch to your fork on Github, the remote `origin`.\n- From your fork open a pull request in the correct branch. Target the project\'s `develop` branch if there is one, else go for `master`!\n- …\n- If the maintainer requests further changes just push them to your branch. The PR will be updated automatically.\n- Once the pull request is approved and merged you can pull the changes from `upstream` to your local repo and delete\n  your extra branch(es).\n\n <!-- CONTACT -->\n\n## Contact\n\nBord4 - bord4@bt.no\n',
    'author': 'Lasse Lambrechts',
    'author_email': 'lasse.lambrechts@bt.no',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
