# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['labelu_ml', 'labelu_ml.examples.the_simplest_app']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'fastapi>=0.88.0,<0.89.0',
 'loguru>=0.6.0,<0.7.0',
 'typer[all]>=0.7.0,<0.8.0',
 'uvicorn>=0.20.0,<0.21.0']

entry_points = \
{'console_scripts': ['labelu-ml = labelu_ml.main:cli']}

setup_kwargs = {
    'name': 'labelu-ml',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Introduction\n## Quickstart\n\n\n1. Setup environment\n    \n    ```bash\n    conda create -n labelu-ml python=3.7\n    conda activate labelu-ml\n    ```\n   \n2. Install labelu-ml\n   ```bash\n   pip install labelu-ml\n   ```\n\n3. Initialize an ML application based on an example path:\n   ```bash\n   labelu-ml init my_ml_app --path labelu_ml/examples/the_simplest_app\n\n   pip install -r my_ml_app/requirements.txt\n   ```\n\n4. Start ML application server\n   ```bash\n   labelu-ml start my_ml_app\n   ```\n\n## Usage\n\n### Command line\n```\n$ labelu-ml --help\n                                                                                                                                                     \n Usage: labelu-ml [OPTIONS] COMMAND [ARGS]...                                                                                                        \n                                                                                                                                                     \n╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮\n│ --install-completion          Install completion for the current shell.                                                                           │\n│ --show-completion             Show completion for the current shell, to copy it or customize the installation.                                    │\n│ --help                        Show this message and exit.                                                                                         │\n╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\n╭─ Commands ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮\n│ init                  Initailize an ML app from a example.                                                                                        │\n│ start                 Start ML app server.                                                                                                        │\n╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\n\n```',
    'author': 'pengjinhu',
    'author_email': 'pengjinhu@pjlab.org.cn',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
