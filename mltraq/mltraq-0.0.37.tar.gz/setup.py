# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mltraq', 'mltraq.extras', 'mltraq.steps', 'mltraq.storage', 'mltraq.utils']

package_data = \
{'': ['*']}

install_requires = \
['certifi>=2022.12.7,<2023.0.0',
 'cloudpickle>=2.2.0,<3.0.0',
 'colorama>=0.4.6,<0.5.0',
 'joblib>=1.2.0,<2.0.0',
 'pandas>=1.5.1,<2.0.0',
 'setuptools>=65.6.3,<66.0.0',
 'sqlalchemy-utils>=0.38.3,<0.39.0',
 'sqlalchemy>=1.4.44,<2.0.0',
 'tqdm>=4.64.1,<5.0.0',
 'ulid-py>=1.1.0,<2.0.0']

extras_require = \
{'complete': ['tabulate>=0.9.0,<0.10.0',
              'ipywidgets>=8.0.2,<9.0.0',
              'scikit-learn>=1.1.3,<2.0.0',
              'dask[complete]>=2022.11.0,<2023.0.0'],
 'dask': ['dask[complete]>=2022.11.0,<2023.0.0'],
 'pgsql': ['psycopg2-binary>=2.9.5,<3.0.0']}

setup_kwargs = {
    'name': 'mltraq',
    'version': '0.0.37',
    'description': 'A lightweight experimentation toolkit for data scientists.',
    'long_description': '<p align="center">\n<img width="33%" height="33%" src="https://mltraq.com/assets/img/logo-black.svg" alt="MLTRAQ Logo">\n</p>\n\n<p align="center">\n<img src="https://www.mltraq.com/assets/img/badges/test.svg" alt="Test">\n<img src="https://www.mltraq.com/assets/img/badges/coverage.svg" alt="Test">\n<img src="https://www.mltraq.com/assets/img/badges/python.svg" alt="Test">\n<img src="https://www.mltraq.com/assets/img/badges/pypi.svg" alt="Test">\n<img src="https://www.mltraq.com/assets/img/badges/license.svg" alt="Test">\n<img src="https://www.mltraq.com/assets/img/badges/code-style.svg" alt="Test">\n</p>\n\n---\n\nOpen source **experiment tracking API** with **ML performance analysis** to build better models faster, facilitating collaboration and transparency within the team and with stakeholders.\n\n---\n\n* **Documentation**: [https://www.mltraq.com](https://www.mltraq.com)\n* **Source code**: [https://github.com/elehcimd/mltraq](https://github.com/elehcimd/mltraq)\n\n---\n\n## Key features\n\n* **Fast and efficient**: start tracking experiments with a few lines of code.\n* **Distributed**: work on experiments independently and upstream them for sharing.\n* **Accessible**: Simple SQL tables queriable with SQL, Pandas and Python API.\n* **Structured types**: track Python types, Numpy arrays, Pandas dataframes and series.\n* **Parallel execution**: define experiments as steps with parameter grids and execute them.\n* **Light checkpointing**: save time by reloading and continuing your experiments anywhere.\n* **Steps library**: enjoy pre-built steps for tracking, testing, analysis and reporting.\n\n## Requirements\n\n* **Python 3.7+**\n* **SQLAlchemy**, **Pandas**, and **Joblib** (installed as dependencies)\n\n## Installation\n\n```\npip install mltraq\n```\n\n## License\n\nThis project is licensed under the terms of the [BSD 3-Clause License](https://mltraq.com/license).\n\n',
    'author': 'Michele Dallachiesa',
    'author_email': 'michele.dallachiesa@sigforge.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/elehcimd/stratosphere',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8.0,<3.11',
}


setup(**setup_kwargs)
