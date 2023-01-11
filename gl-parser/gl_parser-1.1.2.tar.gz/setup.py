# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gl_parser',
 'gl_parser.cli',
 'gl_parser.config',
 'tests',
 'tests.cli',
 'tests.config']

package_data = \
{'': ['*'], 'tests': ['fixtures/*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'openpyxl>=3.0.10,<4.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'toml>=0.10.2,<0.11.0',
 'tqdm>=4.64.1,<5.0.0']

entry_points = \
{'console_scripts': ['gl-parser = gl_parser.cli.cli_commands:main']}

setup_kwargs = {
    'name': 'gl-parser',
    'version': '1.1.2',
    'description': 'General ledger Excel parser and converter..',
    'long_description': '# GL Parser\n\n\n[![pypi](https://img.shields.io/pypi/v/gl-parser.svg)](https://pypi.org/project/gl-parser/)\n[![python](https://img.shields.io/pypi/pyversions/gl-parser.svg)](https://pypi.org/project/gl-parser/)\n[![Build Status](https://github.com/luiscberrocal/gl-parser/actions/workflows/dev.yml/badge.svg)](https://github.com/luiscberrocal/gl-parser/actions/workflows/dev.yml)\n[![codecov](https://codecov.io/gh/luiscberrocal/gl-parser/branch/main/graphs/badge.svg)](https://codecov.io/github/luiscberrocal/gl-parser)\n\n\n\nGeneral ledger Excel parser and converter.\n\n\n* Documentation: <https://luiscberrocal.github.io/gl-parser>\n* GitHub: <https://github.com/luiscberrocal/gl-parser>\n* PyPI: <https://pypi.org/project/gl-parser/>\n* Free software: MIT\n\n\n## Features\n\n* TODO\n\n## Credits\n\nThis package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [waynerv/cookiecutter-pypackage](https://github.com/waynerv/cookiecutter-pypackage) project template.\n',
    'author': 'Luis C. Berrocal',
    'author_email': 'luis.berrocal.1942@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/luiscberrocal/gl-parser',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
