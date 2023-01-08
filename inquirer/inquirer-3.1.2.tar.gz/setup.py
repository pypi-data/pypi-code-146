# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['inquirer', 'inquirer.render', 'inquirer.render.console']

package_data = \
{'': ['*']}

install_requires = \
['blessed>=1.19.0', 'python-editor>=1.0.4', 'readchar>=3.0.6']

setup_kwargs = {
    'name': 'inquirer',
    'version': '3.1.2',
    'description': 'Collection of common interactive command line user interfaces, based on Inquirer.js',
    'long_description': '[![PyPI](https://img.shields.io/pypi/v/inquirer.svg)][pypi status]\n[![Status](https://img.shields.io/pypi/status/inquirer.svg)][pypi status]\n[![Python Version](https://img.shields.io/pypi/pyversions/inquirer)][pypi status]\n[![License](https://img.shields.io/pypi/l/inquirer)][license]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n<br>\n[![Read the documentation at https://python-inquirer.readthedocs.io/](https://img.shields.io/readthedocs/python-inquirer/latest.svg?label=Read%20the%20Docs)][read the docs]\n[![Tests](https://github.com/magmax/python-inquirer/workflows/Tests/badge.svg)][tests]\n[![Codecov](https://codecov.io/gh/magmax/python-inquirer/branch/main/graph/badge.svg)][codecov]\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n\n[pypi status]: https://pypi.org/project/inquirer/\n[read the docs]: https://python-inquirer.readthedocs.io/\n[tests]: https://github.com/magmax/python-inquirer/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/magmax/python-inquirer\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\n# python-inquirer\n\nCollection of common interactive command line user interfaces, based on [Inquirer.js].\n\n## Goal and Philosophy\n\nBorn as a [Inquirer.js] clone, it shares part of the goals and philosophy.\n\nSo, **Inquirer** should ease the process of asking end user **questions**, **parsing**, **validating** answers, managing **hierarchical prompts** and providing **error feedback**.\n\nYou can [download the python-inquirer code from GitHub] or [download the wheel from Pypi].\n\n### Platforms support\n\nPython-inquirer supports mainly UNIX-based platforms (eq. Mac OS, Linux, etc.). Windows has experimental support, please let us know if there are any problems!\n\n## Installation\n\n```sh\npip install inquirer\n```\n\n## Documentation\n\nDocumentation has been moved to [magmax.org/python-inquirer](https://magmax.org/python-inquirer/).\n\nBut here you have a couple of usage examples:\n\n### Text\n\n```python\nimport re\n\nimport inquirer\nquestions = [\n  inquirer.Text(\'name\', message="What\'s your name"),\n  inquirer.Text(\'surname\', message="What\'s your surname"),\n  inquirer.Text(\'phone\', message="What\'s your phone number",\n                validate=lambda _, x: re.match(\'\\+?\\d[\\d ]+\\d\', x),\n                )\n]\nanswers = inquirer.prompt(questions)\n```\n\n### Editor\n\nLike a Text question, but used for larger answers. It opens external text editor which is used to collect the answer.\n\nThe environment variables $VISUAL and $EDITOR, can be used to specify which editor should be used. If not present inquirer fallbacks to `vim -> emacs -> nano` in this order based on availability in the system.\n\nExternal editor handling is done using great library [python-editor](https://github.com/fmoo/python-editor).\n\nExample:\n\n```python\nimport inquirer\nquestions = [\n  inquirer.Editor(\'long_text\', message="Provide long text")\n]\nanswers = inquirer.prompt(questions)\n```\n\n### List\n\nShows a list of choices, and allows the selection of one of them.\n\nExample:\n\n```python\nimport inquirer\nquestions = [\n  inquirer.List(\'size\',\n                message="What size do you need?",\n                choices=[\'Jumbo\', \'Large\', \'Standard\', \'Medium\', \'Small\', \'Micro\'],\n            ),\n]\nanswers = inquirer.prompt(questions)\n```\n\nList questions can take one extra argument `carousel=False`. If set to true, the answers will rotate (back to first when pressing down on last choice, and down to last choice when pressing up on first choice)\n\n### Checkbox\n\nShows a list of choices, with multiple selection.\n\nExample:\n\n```python\nimport inquirer\nquestions = [\n  inquirer.Checkbox(\'interests\',\n                    message="What are you interested in?",\n                    choices=[\'Computers\', \'Books\', \'Science\', \'Nature\', \'Fantasy\', \'History\'],\n                    ),\n]\nanswers = inquirer.prompt(questions)\n```\n\nCheckbox questions can take one extra argument `carousel=False`. If set to true, the answers will rotate (back to first when pressing down on last choice, and down to last choice when pressing up on first choice)\n\n### Path\n\nLike Text question, but with builtin validations for working with paths.\n\nExample:\n\n```python\nimport inquirer\nquestions = [\n  inquirer.Path(\'log_file\',\n                 message="Where logs should be located?",\n                 path_type=inquirer.Path.DIRECTORY,\n                ),\n]\nanswers = inquirer.prompt(questions)\n```\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide].\n\n## License\n\nCopyright (c) 2014-2021 Miguel Ángel García ([@magmax_en]), based on [Inquirer.js], by Simon Boudrias ([@vaxilart])\n\nDistributed under the terms of the [MIT license][license].\n\n<!-- github-only -->\n\n[license]: https://github.com/magmax/python-inquirer/blob/main/LICENSE\n[@magmax_en]: https://twitter.com/magmax_en\n[@vaxilart]: https://twitter.com/vaxilart\n[contributor guide]: CONTRIBUTING.md\n[download the python-inquirer code from github]: https://github.com/magmax/python-inquirer\n[download the wheel from pypi]: https://pypi.python.org/pypi/inquirer\n[examples/]: https://github.com/magmax/python-inquirer/tree/master/examples\n[inquirer.js]: https://github.com/SBoudrias/Inquirer.js\n',
    'author': 'Miguel Ángel García',
    'author_email': 'miguelangel.garcia@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/magmax/python-inquirer',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
