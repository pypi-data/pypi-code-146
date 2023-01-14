# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stage_left']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'stage-left',
    'version': '0.2.1',
    'description': 'Parse [x]it! documents into python data structures',
    'long_description': '# stage-left\n\n[![Run tests](https://github.com/chris48s/stage-left/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/chris48s/stage-left/actions/workflows/test.yml)\n[![codecov](https://codecov.io/gh/chris48s/stage-left/branch/master/graph/badge.svg?token=XS70M8EPCT)](https://codecov.io/gh/chris48s/stage-left)\n[![PyPI Version](https://img.shields.io/pypi/v/stage-left.svg)](https://pypi.org/project/stage-left/)\n![License](https://img.shields.io/pypi/l/stage-left.svg)\n![Python Compatibility](https://img.shields.io/badge/dynamic/json?query=info.requires_python&label=python&url=https%3A%2F%2Fpypi.org%2Fpypi%2Fstage-left%2Fjson)\n![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)\n\n[[x]it!](https://xit.jotaen.net/) is a plain-text file format for todos and check lists. Stage-left parses [x]it! documents into python data structures.\n\n## 📚 [Documentation](https://chris48s.github.io/stage-left/)\n* [Usage Examples](https://chris48s.github.io/stage-left/usage.html)\n* [API Reference](https://chris48s.github.io/stage-left/reference.html)\n',
    'author': 'chris48s',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/chris48s/stage-left',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
