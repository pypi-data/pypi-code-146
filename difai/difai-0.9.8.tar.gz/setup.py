# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['difai']

package_data = \
{'': ['*']}

install_requires = \
['nbconvert>=7.0.0,<8.0.0',
 'nbformat>=5.6.0,<6.0.0',
 'pip-tools>=6.8.0,<7.0.0',
 'typer>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['difai = difai.main:app']}

setup_kwargs = {
    'name': 'difai',
    'version': '0.9.8',
    'description': "'Did I forget any imports' generates requirement files for you",
    'long_description': '# Did I forget any imports?\n\n[![pipeline status](https://gitlab.com/marvin.vanaalst/difai/badges/main/pipeline.svg)](https://gitlab.com/marvin.vanaalst/difai/-/commits/main)\n[![coverage report](https://gitlab.com/marvin.vanaalst/difai/badges/main/coverage.svg)](https://gitlab.com/marvin.vanaalst/difai/-/commits/main)\n[![PyPi](https://img.shields.io/pypi/v/difai)](https://pypi.org/project/difai/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)\n[![Downloads](https://pepy.tech/badge/difai)](https://pepy.tech/project/difai)\n\nDIFAI searches for import statements for all the python and jupyter notebook files in the current directory. It then uses `pip freeze` to get your installed versions and `pip-compile` to generate a `requirements.txt` file containing all of your dependencies and their depdendencies including hashes for a reproducible build.\n\n## Run\n\nSimply call `difai` in the current folder.\nYou can change the input (where the `.py` and `.ipynb` files are read) and output (where the `requirement.in` and `requirements.txt` files are written) folders using\n`--in-path` and `--out-path` respectively.\nIn order to exclude certain packages from the search, you can use the `--exclude` option.\n\n## Pipeline\n\n<div class="center">\n\n```mermaid\ngraph TB\n    A[glob] --> B\n    A --> C\n    B[.py] --> D\n    C[.ipynb] -->|nbconvert| B\n    D[AST]  --> E\n    X[pip freeze] --> E\n    E[requirements.in] -->|pip tools| F\n    F[requirements.txt]\n```\n\n</div>\n',
    'author': 'Marvin van Aalst',
    'author_email': 'marvin.vanaalst@gmail.com',
    'maintainer': 'Marvin van Aalst',
    'maintainer_email': 'marvin.vanaalst@gmail.com',
    'url': 'https://gitlab.com/marvin.vanaalst/difai',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
