# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyella']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyella',
    'version': '1.1.1',
    'description': 'This library brings common monads such `Maybe` and `Either` to your Python projects.',
    'long_description': '# Pyella\n\n[![License: MPL 2.0](https://img.shields.io/badge/License-MPL%202.0-brightgreen.svg)](https://opensource.org/licenses/MPL-2.0)\n[![Build](https://github.com/edeckers/pyella/actions/workflows/test.yml/badge.svg?branch=develop)](https://github.com/edeckers/pyella/actions/workflows/test.yml)\n[![PyPI](https://img.shields.io/pypi/v/pyella.svg?maxAge=3600)](https://pypi.org/project/pyella)\n[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)\n\nThis library brings common monads such as `Maybe` and `Either` to your Python projects.\n\n## Requirements\n\n- Python 3.7+\n\n## Installation\n\n```bash\npip3 install pyella\n```\n\n## Usage\n\n### Maybe\n\nThe snippet below demonstrates some of the oprations that are available for `Maybe`.\n\n```python\nfrom pyella.maybe import Maybe\n\nj0 = Maybe.of(1)\nprint (j0)\n# Output: Just(1)\n\nprint (j0.from_maybe(-1))\n# Output: 1\n\nj1 = j0.fmap(lambda x:x*2)\nprint(j0)\nprint(j1)\n# Output:\n#\n# Just(1)\n# Just(2)\n```\n\n### Either\n\nAnd these are some things you can do with `Either`.\n\n```python\nfrom pyella.either import Either, left, lefts, right, rights\n\ne0: Either[str, int] = left("invalid value")\nprint(e0)\n# Output: Left(invalid value)\n\nprint (e0.if_left(-1))\nprint (e0.if_right("the value was valid"))\n# Output:\n#\n# -1\n# \'invalid value\'\n\ne1: Either[str, int] = right(1)\nprint (e1)\n# Output: Right(1)\n\ne2 = e1.fmap(lambda x:x*2)\nprint(e1)\nprint(e2)\n# Output:\n#\n# Right(1)\n# Right(2)\n\nvalid_values = rights([e0, e1, e2])\nprint (valid_values)\n# Output: [1, 2]\n```\n\n\n## Contributing\n\nSee the [contributing guide](CONTRIBUTING.md) to learn how to contribute to the  repository and the development workflow.\n\n## Code of Conduct\n\n[Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.\n\n## License\n\nMPL-2.0\n',
    'author': 'Ely Deckers',
    'author_email': 'None',
    'maintainer': 'Ely Deckers',
    'maintainer_email': 'None',
    'url': 'https://github.com/edeckers/pyella.git',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
