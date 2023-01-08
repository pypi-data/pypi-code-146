# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nba_data_miner']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'helper-functions>=2.0.11,<3.0.0',
 'html5lib>=1.1,<2.0',
 'numpy>=1.23.5,<2.0.0',
 'pandas>=1.5.2,<2.0.0',
 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'nba-data-miner',
    'version': '0.1.0',
    'description': 'A package to help with searching and comparing players and teams in the NBA.',
    'long_description': '# nba_data_miner\n\nA package to help with searching and comparing players and teams in the NBA.\n\n## Installation\n\n```bash\n$ pip install nba_data_miner\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`nba_data_miner` was created by Francis Baring. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`nba_data_miner` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Francis Baring',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/frank-baring',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
