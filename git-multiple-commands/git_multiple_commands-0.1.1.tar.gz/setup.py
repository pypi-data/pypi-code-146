# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['git_multiple_commands']

package_data = \
{'': ['*']}

install_requires = \
['pyyaml>=6.0,<7.0', 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['gmc = git_multiple_commands.gmc:app']}

setup_kwargs = {
    'name': 'git-multiple-commands',
    'version': '0.1.1',
    'description': 'Run git commands in multiple directories at once',
    'long_description': '[![pipeline status](https://gitlab.com/kisphp/python-cli-tool/badges/main/pipeline.svg)](https://gitlab.com/kisphp/python-cli-tool/-/commits/main)\n[![coverage report](https://gitlab.com/kisphp/python-cli-tool/badges/main/coverage.svg)](https://gitlab.com/kisphp/python-cli-tool/-/commits/main)\n\nRun got commands in multiple directories at once.\n\n```bash\ngmc # show help message\ngmc build # generate .gmc.yaml file\ngmc i # git init in all directories\n```\n\n# Install\n\n```bash\npip install -U git-multiple-commands\n```',
    'author': 'Bogdan Rizac',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
