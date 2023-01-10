# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cherno', 'cherno.actor', 'cherno.actor.commands']

package_data = \
{'': ['*'], 'cherno': ['etc/*']}

install_requires = \
['astropy>=5.0.0,<6.0.0',
 'click-default-group>=1.2.2,<2.0.0',
 'pandas>=1.3.4,<2.0.0',
 'photutils>=1.3.0,<2.0.0',
 'psycopg2-binary>=2.9.5,<3.0.0',
 'sdss-clu>=1.8.0,<2.0.0',
 'sdss-coordio>=1.5.2,<2.0.0',
 'sdsstools>=1.0.0,<2.0.0',
 'simple-pid>=1.0.1,<2.0.0',
 'sqlalchemy>=1.4.45,<2.0.0',
 'tables>=3.6.1']

entry_points = \
{'console_scripts': ['cherno = cherno.__main__:cherno']}

setup_kwargs = {
    'name': 'sdss-cherno',
    'version': '0.5.1',
    'description': 'SDSS guider actor',
    'long_description': '# cherno\n\n![Versions](https://img.shields.io/badge/python->3.8-blue)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Documentation Status](https://readthedocs.org/projects/sdss-cherno/badge/?version=latest)](https://sdss-cherno.readthedocs.io/en/latest/?badge=latest)\n[![Tests Status](https://github.com/sdss/cherno/workflows/Test/badge.svg)](https://github.com/sdss/cherno/actions)\n[![codecov](https://codecov.io/gh/sdss/cherno/branch/main/graph/badge.svg)](https://codecov.io/gh/sdss/cherno)\n\n\nSDSS guider actor\n\n## Installation\n\nIn general you should be able to install ``cherno`` by doing\n\n```console\npip install sdss-cherno\n```\n\nTo build from source, use\n\n```console\ngit clone git@github.com:sdss/cherno\ncd cherno\npip install .\n```\n\n## Development\n\n`cherno` uses [poetry](http://poetry.eustace.io/) for dependency management and packaging. To work with an editable install it\'s recommended that you setup `poetry` and install `cherno` in a virtual environment by doing\n\n```console\npoetry install\n```\n\n### Style and type checking\n\nThis project uses the [black](https://github.com/psf/black) code style with 88-character line lengths for code and docstrings. It is recommended that you run `black` on save. Imports must be sorted using [isort](https://pycqa.github.io/isort/). The GitHub test workflow checks all the Python file to make sure they comply with the black formatting.\n\nConfiguration files for [flake8](https://flake8.pycqa.org/en/latest/), [isort](https://pycqa.github.io/isort/), and [black](https://github.com/psf/black) are provided and will be applied by most editors. For Visual Studio Code, the following project file is compatible with the project configuration:\n\n```json\n{\n    "python.formatting.provider": "black",\n    "[python]" : {\n        "editor.codeActionsOnSave": {\n            "source.organizeImports": true\n        },\n        "editor.formatOnSave": true\n    },\n    "[markdown]": {\n        "editor.wordWrapColumn": 88\n    },\n    "[restructuredtext]": {\n        "editor.wordWrapColumn": 88\n    },\n    "editor.rulers": [88],\n    "editor.wordWrapColumn": 88,\n    "python.analysis.typeCheckingMode": "basic"\n}\n```\n\nThis assumes that the [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) and [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) extensions are installed.\n\nThis project uses [type hints](https://docs.python.org/3/library/typing.html). Typing is enforced by the test workflow using [pyright](https://github.com/microsoft/pyright) (in practice this means that if ``Pylance`` doesn\'t produce any errors in basic mode, ``pyright`` shouldn\'t).\n',
    'author': 'José Sánchez-Gallego',
    'author_email': 'gallegoj@uw.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sdss/cherno',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
