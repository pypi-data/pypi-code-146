# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ni_python_styleguide',
 'ni_python_styleguide._acknowledge_existing_errors',
 'ni_python_styleguide._utils']

package_data = \
{'': ['*']}

install_requires = \
['black>=22.3,!=22.10.0',
 'click>=7.1.2',
 'flake8-black>=0.2.1',
 'flake8-docstrings>=1.5.0',
 'flake8-import-order>=0.18.1',
 'flake8>=5.0,<6.0',
 'isort>=5.10',
 'pep8-naming>=0.11.1',
 'toml>=0.10.1']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata<5.0']}

entry_points = \
{'console_scripts': ['ni-python-styleguide = ni_python_styleguide._cli:main']}

setup_kwargs = {
    'name': 'ni-python-styleguide',
    'version': '0.3.0',
    'description': "NI's internal and external Python linter rules and plugins",
    'long_description': '# NI Python Style Guide\n\n![logo](https://raw.githubusercontent.com/ni/python-styleguide/main/docs/logo.svg)\n\n---\n\n[![PyPI version](https://badge.fury.io/py/ni-python-styleguide.svg)](https://badge.fury.io/py/ni-python-styleguide) ![Publish Package](https://github.com/ni/python-styleguide/workflows/Publish%20Package/badge.svg) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n\nWelcome to NI\'s internal and external Python conventions and enforcement tooling.\n\n## Written Conventions\n\nOur written conventions can be found at https://ni.github.io/python-styleguide/.\n\nTheir source is in [docs/Coding-Conventions.md](https://github.com/ni/python-styleguide/tree/main/docs/Coding-Conventions.md).\n\nNOTE: Using the GitHub Pages link is preferable to a GitHub `/blob` link.\n\n## Enforcement tooling\n\nAs a tool, `ni-python-styleguide` is installed like any other script:\n\n```bash\npip install ni-python-styleguide\n```\n\n### Linting\n\nTo lint, just run the `lint` subcommand (from within the project root, or lower):\n\n```bash\nni-python-styleguide lint\n# or\nni-python-styleguide lint ./dir/\n# or\nni-python-styleguide lint module.py\n```\n\nThe rules enforced are all rules documented in the written convention, which are marked as enforced.\n\n### Configuration\n\n`ni-python-styleguide` aims to keep the configuration to a bare minimum (none wherever possible).\nHowever there are some situations you might need to configure the tool.\n\n#### When using `setup.py`\n\nIf you\'re using `setup.py`, you\'ll need to set your app\'s import names for import sorting.\n\n```toml\n# pyproject.toml\n[tool.ni-python-styleguide]\napplication-import-names = "<app_name>"\n```\n\n### Formatting\n\n`ni-python-styleguide` in the future will have a `format` command which we intend to fix as many lint issues as possible.\n\nUntil then you\'ll want to set the following to get `black` formatting as the styleguide expects.\n\n```toml\n# pyproject.toml\n[tool.black]\nline-length = 100\n```\n\n### Editor Integration\n\n(This section to come!)\n',
    'author': 'NI',
    'author_email': 'opensource@ni.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ni/python-styleguide',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
