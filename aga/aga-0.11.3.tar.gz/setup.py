# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aga', 'aga.cli', 'aga.gradescope', 'aga.gradescope.resources']

package_data = \
{'': ['*']}

install_requires = \
['dacite>=1.6.0,<2.0.0',
 'dataclasses-json>=0.5.6,<0.6.0',
 'dill>=0.3.4,<0.4.0',
 'gradescope-utils>=0.4.0,<0.5.0',
 'toml>=0.10.2,<0.11.0',
 'typer[all]>=0.6.1,<0.7.0',
 'types-toml>=0.10.8,<0.11.0']

entry_points = \
{'console_scripts': ['aga = aga.cli:aga_app']}

setup_kwargs = {
    'name': 'aga',
    'version': '0.11.3',
    'description': 'aga grades assignments',
    'long_description': '<div align="center">\n\n# aga grades assignments\n\n[![tests](https://github.com/nihilistkitten/aga/workflows/tests/badge.svg)](https://github.com/nihilistkitten/aga/actions?workflow=tests)\n[![lints](https://github.com/nihilistkitten/aga/workflows/lints/badge.svg)](https://github.com/nihilistkitten/aga/actions?workflow=lints)\n[![Codecov](https://codecov.io/gh/nihilistkitten/aga/branch/main/graph/badge.svg)](https://codecov.io/gh/nihilistkitten/aga)\n[![PyPI](https://img.shields.io/pypi/v/aga.svg)](https://pypi.org/project/aga/)\n[![Read the Docs](https://readthedocs.org/projects/aga/badge/)](https://aga.readthedocs.io/)\n[![License](https://img.shields.io/github/license/nihilistkitten/aga)](https://choosealicense.com/licenses/mit/)\n\n</div>\n\n**aga** (**a**ga **g**rades **a**ssignments) is a tool for easily producing autograders for python programming assignments, originally developed for Reed College\'s CS1 course.\n\n## Motivation\n\nUnlike traditional software testing, where there is likely no _a priori_ known-correct implementation, there is always such an implementation (or one can be easily written by course staff) in homework grading. Therefore, applying traditional software testing frameworks to homework grading is limited. Relying on reference implementations (what aga calls _golden solutions_) has several benefits:\n\n1. Reliability: having a reference solution gives a second layer of confirmation for the correctness of expected outputs. Aga supports _golden tests_, which function as traditional unit tests of the golden solution.\n2. Test case generation: many complex test cases can easily be generated via the reference solution, instead of needing to work out the expected output by hand. Aga supports generating test cases from inputs without explcitly referring to an expected output, and supports collecting test cases from python generators.\n3. Property testing: unit testing libraries like [hypothesis](https://hypothesis.readthedocs.io) allow testing large sets of arbitrary inputs for certain properties, and identifying simple inputs which reproduce violations of those properties. This is traditionally unreliable, because identifying specific properties to test is difficult. In homework grading, the property can simply be "the input matches the golden solution\'s output." Support for hypothesis is a [long-term goal](https://github.com/nihilistkitten/aga/issues/32) of aga.\n\n## Installation\n\nInstall from pip:\n\n```bash\npip install aga\n```\n\nor with the python dependency manager of your choice (I like [poetry](https://github.com/python-poetry/poetry)), for example:\n\n```bash\ncurl -sSL https://install.python-poetry.org | python3 -\necho "cd into aga repo"\ncd aga\npoetry install && poetry shell\n```\n\n## Example\n\nIn `square.py` (or any python file), write:\n\n```python\nfrom aga import problem, test_case, test_cases\n\n@test_cases([-3, 100])\n@test_case(2, aga_expect=4)\n@test_case(-2, aga_expect=4)\n@problem()\ndef square(x: int) -> int:\n    """Square x."""\n    return x * x\n```\n\nThen run `aga gen square.py` from the directory with `square.py`. This will generate a ZIP file suitable for upload to Gradescope.\n\n## Usage\n\nAga relies on the notion of a _golden solution_ to a given problem which is known to be correct. The main work of the library is to compare the output of this golden solution on some family of test inputs against the output of a student submission. To that end, aga integrates with frontends: existing classroom software which allow submission of student code. Currently, only Gradescope is supported.\n\nTo use aga:\n\n1. Write a golden solution to some programming problem.\n2. Decorate this solution with the `problem` decorator.\n3. Decorate this problem with any number of `test_case` decorators, which take arbitrary positional or keyword arguments and pass them verbatim to the golden and submitted functions.\n4. Generate the autograder using the CLI: `aga gen <file_name>`.\n\nThe `test_case` decorator may optionally take a special keyword argument called `aga_expect`. This allows easy testing of the golden solution: aga will not successfully produce an autograder unless the golden solution\'s output matches the `aga_expect`. You should use these as sanity checks to ensure your golden solution is implemented correctly.\n\nFor more info, see the [tutorial](https://aga.readthedocs.io/en/stable/tutorial.html).\n\nFor complete documentation, including configuring problem and test case metadata, see the [API reference](https://aga.readthedocs.io/en/stable/reference.html).\n\nFor CLI documentation, run `aga --help`, or access the docs [online](https://aga.readthedocs.io/en/stable/cli.html).\n\n## Contributing\n\nBug reports, feature requests, and pull requests are all welcome. For details on our test suite, development environment, and more, see the [developer documentation](https://aga.readthedocs.io/en/stable/development.html).\n\n<!-- vim:set tw=0: -->\n',
    'author': 'Riley Shahar',
    'author_email': 'riley.shahar@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/nihilistkitten/aga',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10.0,<4.0.0',
}


setup(**setup_kwargs)
