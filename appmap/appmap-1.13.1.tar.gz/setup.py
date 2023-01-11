# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'vendor/wrapt/src'}

packages = \
['_appmap',
 '_appmap.test',
 '_appmap.test.data',
 '_appmap.test.data.appmap_testing',
 '_appmap.test.data.config-exclude..hide.hidden_mod',
 '_appmap.test.data.config-exclude.node_modules.node_mod',
 '_appmap.test.data.config-exclude.src.package',
 '_appmap.test.data.config-exclude.test',
 '_appmap.test.data.config-exclude.venv.venv_mod',
 '_appmap.test.data.config.src.package',
 '_appmap.test.data.config.test',
 '_appmap.test.data.django',
 '_appmap.test.data.django.app',
 '_appmap.test.data.django.init',
 '_appmap.test.data.django.test',
 '_appmap.test.data.flask',
 '_appmap.test.data.flask.init',
 '_appmap.test.data.package1',
 '_appmap.test.data.package1.package2',
 '_appmap.test.data.pytest',
 '_appmap.test.data.trial.init',
 '_appmap.test.data.trial.test',
 '_appmap.test.data.unittest.init',
 '_appmap.test.data.unittest.simple',
 'appmap',
 'appmap.command',
 'appmap.labeling',
 'wrapt']

package_data = \
{'': ['*'],
 '_appmap.test.data': ['trial/*',
                       'trial/expected/*',
                       'unittest/*',
                       'unittest/expected/*'],
 '_appmap.test.data.flask': ['templates/*'],
 '_appmap.test.data.pytest': ['expected/*']}

install_requires = \
['PyYAML>=5.3.0',
 'importlib-metadata>=0.8',
 'importlib-resources>=5.4.0,<6.0.0',
 'inflection>=0.3.0',
 'packaging>=21.3,<22.0']

entry_points = \
{'console_scripts': ['appmap-agent-init = appmap.command.appmap_agent_init:run',
                     'appmap-agent-status = '
                     'appmap.command.appmap_agent_status:run',
                     'appmap-agent-validate = '
                     'appmap.command.appmap_agent_validate:run'],
 'pytest11': ['appmap = appmap.pytest']}

setup_kwargs = {
    'name': 'appmap',
    'version': '1.13.1',
    'description': 'Create AppMap files by recording a Python application.',
    'long_description': '- [About](#about)\n- [Usage](#usage)\n- [Development](#development)\n  - [Getting the code](#getting-the-code)\n  - [Python version support](#python-version-support)\n  - [Dependency management](#dependency-management)\n  - [Linting](#linting)\n  - [Testing](#testing)\n    - [pytest](#pytest)\n    - [tox](#tox)\n  - [Code Coverage](#code-coverage)\n\n# About\n`appmap-python` is a Python package for recording\n[AppMaps](https://github.com/applandinc/appmap) of your code. "AppMap" is a data format\nwhich records code structure (modules, classes, and methods), code execution events\n(function calls and returns), and code metadata (repo name, repo URL, commit SHA, labels,\netc). It\'s more granular than a performance profile, but it\'s less granular than a full\ndebug trace. It\'s designed to be optimal for understanding the design intent and structure\nof code and key data flows.\n\n# Usage\n\nVisit the [AppMap for Python](https://appland.com/docs/reference/appmap-python.html) reference page on AppLand.com for a complete reference guide.\n\n# Development\n\n[![Build Status](https://travis-ci.com/applandinc/appmap-python.svg?branch=master)](https://travis-ci.com/applandinc/appmap-python)\n\n## Getting the code\nClone the repo to begin development. Note that vendored dependencies are included as\nsubmodules.\n\n```shell\n% git clone --recurse-submodules https://github.com/applandinc/appmap-python.git\nCloning into \'appmap-python\'...\nremote: Enumerating objects: 167, done.\nremote: Counting objects: 100% (167/167), done.\nremote: Compressing objects: 100% (100/100), done.\nremote: Total 962 (delta 95), reused 116 (delta 61), pack-reused 795\nReceiving objects: 100% (962/962), 217.31 KiB | 4.62 MiB/s, done.\nResolving deltas: 100% (653/653), done.\nSubmodule \'extern/wrapt\' (https://github.com/applandinc/wrapt.git) registered for path \'vendor/wrapt\'\nCloning into \'/private/tmp/appmap-python/vendor/wrapt\'...\nremote: Enumerating objects: 46, done.\nremote: Counting objects: 100% (46/46), done.\nremote: Compressing objects: 100% (39/39), done.\nremote: Total 2537 (delta 9), reused 19 (delta 4), pack-reused 2491\nReceiving objects: 100% (2537/2537), 755.94 KiB | 7.48 MiB/s, done.\nResolving deltas: 100% (1643/1643), done.\nSubmodule path \'vendor/wrapt\': checked out \'9bdfbe54b88a64069cba1f3c36e77edc3c1339c9\'\n\n% ls appmap-python/vendor/wrapt\nLICENSE\t\tMakefile\tappveyor.yml\tdocs\t\tsrc\t\ttests\nMANIFEST.in\tREADME.rst\tblog\t\tsetup.py\ttddium.yml\ttox.ini\n```\n\n## Python version support\nAs a package intended to be installed in as many environments as possible, `appmap-python`\nneeds to avoid using features of Python or the standard library that were added after the\noldest version currently supported (see the\n[supported versions](https://appland.com/docs/reference/appmap-python.html#supported-versions)).\n\n## Dependency management\n\n[poetry](https://https://python-poetry.org/) for dependency management:\n\n```\n% brew install poetry\n% cd appmap-python\n% poetry install\n```\n\n## Linting\n[pylint](https://www.pylint.org/) for linting:\n\n```\n% cd appmap-python\n% poetry run pylint appmap\n\n--------------------------------------------------------------------\nYour code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)\n\n```\n\n[Note that the current configuration requires a 10.0 for the Travis build to pass. To make\nthis easier to achieve, convention and refactoring checks have both been disabled. They\nshould be reenabled as soon as possible.]\n\n\n## Testing\n### pytest\n\nNote that you must install the dependencies contained in\n[requirements-test.txt](requirements-test.txt) before running tests. See the explanation in\n[pyproject.toml](pyproject.toml) for details.\n\n[pytest](https://docs.pytest.org/en/stable/) for testing:\n\n```\n% cd appmap-python\n% pip install -r requirements-test.txt\n% poetry run pytest\n```\n\n### tox\nAdditionally, the `tox` configuration provides the ability to run the tests for all\nsupported versions of Python and djanggo. \n\n`tox` requires that all the correct versions of Python to be available to create\nthe test environments. [pyenv](https://github.com/pyenv/pyenv) is an easy way to manage\nmultiple versions of Python, and the [xxenv-latest\nplugin](https://github.com/momo-lab/xxenv-latest) can help get all the latest versions.\n\n\n\n```sh\n% brew install pyenv\n% git clone https://github.com/momo-lab/xxenv-latest.git "$(pyenv root)"/plugins/xxenv-latest\n% cd appmap-python\n% pyenv latest local 3.{9,6,7,8}\n% for v in 3.{9,6,7,8}; do pyenv latest install $v; done\n% poetry run tox\n```\n\n## Code Coverage\n[coverage](https://coverage.readthedocs.io/) for coverage:\n\n```\n% cd appmap-python\n% poetry run coverage run -m pytest\n% poetry run coverage html\n% open htmlcov/index.html\n```\n',
    'author': 'Alan Potter',
    'author_email': 'alan@app.land',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/applandinc/appmap-python',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
