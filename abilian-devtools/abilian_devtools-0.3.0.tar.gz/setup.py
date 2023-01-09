# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['abilian', 'abilian.devtools']

package_data = \
{'': ['*']}

install_requires = \
['black',
 'deptry',
 'docformatter',
 'flake8-assertive',
 'flake8-bandit',
 'flake8-breakpoint',
 'flake8-bugbear',
 'flake8-cognitive-complexity',
 'flake8-comprehensions',
 'flake8-datetimez',
 'flake8-functions',
 'flake8-if-expr',
 'flake8-isort',
 'flake8-logging-format',
 'flake8-mutable',
 'flake8-no-pep420',
 'flake8-pep3101',
 'flake8-pep585',
 'flake8-pep604',
 'flake8-pytest',
 'flake8-pytest-style',
 'flake8-simplify',
 'flake8-super',
 'flake8-super-call',
 'flake8-tidy-imports',
 'flake8-tuple',
 'flake8>=6,<7',
 'isort',
 'mypy',
 'nox',
 'pep8-naming',
 'pip',
 'pip-audit',
 'pre-commit',
 'profilehooks',
 'pyright',
 'pytest-cov>=4,<5',
 'pytest-random-order',
 'pytest-xdist',
 'pytest>=7,<8',
 'reuse',
 'ruff',
 'safety',
 'typer',
 'vulture']

entry_points = \
{'console_scripts': ['adt = abilian.devtools.main:app']}

setup_kwargs = {
    'name': 'abilian-devtools',
    'version': '0.3.0',
    'description': 'A curated set of dependencies for quality software development',
    'long_description': "Abilian Development Tools\n=========================\n\nWhat this is?\n-------------\n\nThis is a curated, and opiniated, collection of best-of-breed Python development tools:\n\n- Formatters (`black`, `isort`, `docformatter`)\n- Testing frameworks (`pytest` and friends, `nox`)\n- Style checkers (`ruff`, `flake8` and friends)\n- Type checkers (`mypy`, `pyright`)\n- Supply chain audit (`pip-audit`, `safety`, `reuse`, `vulture`, `deptry`)\n- And more.\n\nUsage\n-----\n\nInstead of having to track all the 40+ projects and plugins we have curated, you just need to add `abilian-devtools = '*'` in your project's `requirements.in` or `pyproject.toml`.\n\nYou still need to properly configure and call them in your own projects.\n\nFor example configuration, see, for instance, <https://github.com/abilian/nua> (`Makefile`, `pyproject.toml`, `setup.cfg`).\n\nAs a bonus, we're providing a CLI called `adt` which can help you get started:\n\n```\n$ adt --help\nUsage: adt [OPTIONS] COMMAND [ARGS]...\n\nAbilian Dev Tool command-line runner.\n\n╭─ Options ────────────────────────────────────────────────────────────────────╮\n│ --install-completion        [bash|zsh|fish|powershe  Install completion for  │\n│                             ll|pwsh]                 the specified shell.    │\n│                                                      [default: None]         │\n│ --show-completion           [bash|zsh|fish|powershe  Show completion for the │\n│                             ll|pwsh]                 specified shell, to     │\n│                                                      copy it or customize    │\n│                                                      the installation.       │\n│                                                      [default: None]         │\n│ --help                                               Show this message and   │\n│                                                      exit.                   │\n╰──────────────────────────────────────────────────────────────────────────────╯\n╭─ Commands ───────────────────────────────────────────────────────────────────╮\n│ all               Run everything.                                            │\n│ check             Run checker/linters on specified files or directories.     │\n│ security-check    Run security checks.                                       │\n│ test              Run tests.                                                 │\n╰──────────────────────────────────────────────────────────────────────────────╯\n```\n",
    'author': 'Stefane Fermigier',
    'author_email': 'sf@abilian.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/abilian/abilian-devtools',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
