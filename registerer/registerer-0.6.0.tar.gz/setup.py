# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['registerer']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'registerer',
    'version': '0.6.0',
    'description': 'Everything you need to implement maintainable and easy to use registry patterns in your project.',
    'long_description': '# Registerer\n\n[![pypi](https://img.shields.io/pypi/v/registerer.svg)](https://pypi.python.org/pypi/registerer/)\n[![ci](https://github.com/danialkeimasi/python-registerer/workflows/ci/badge.svg)](https://github.com/danialkeimasi/python-registerer/actions)\n[![codecov](https://codecov.io/gh/danialkeimasi/python-registerer/branch/main/graph/badge.svg?token=Q5MG14RKJL)](https://codecov.io/gh/danialkeimasi/python-registerer)\n[![license](https://img.shields.io/github/license/danialkeimasi/python-registerer.svg)](https://github.com/danialkeimasi/python-registerer/blob/master/LICENSE)\n\nImplement maintainable and easy to use registry patterns in your project.\n\n## TLDR\n\nWrite this:\n\n```python exec="true" source="above"\nimport registerer\n\ncommand_handler_registry = registerer.Registerer()\n\n\n@command_handler_registry.register()\ndef info(args):\n    return "how can i help you?"\n\n\n@command_handler_registry.register()\ndef play(args):\n    return "let me play a song for you"\n\n\ncommand = "info"\nargs = {}\nassert command_handler_registry[command](args) == "how can i help you?"\n```\n\nInstead of this, which violates the Open-Closed Principle (OCP):\n\n```python exec="true" source="above"\ndef info(args):\n    return "how can i help you?"\n\n\ndef play(args):\n    return "let me play a song for you"\n\n\ndef command_handler(command, args):\n    if command == "info":\n        return info(args)\n    if command == "play":\n        return play(args)\n\n\ncommand = "play"\nargs = {}\nassert command_handler(command, args) == "let me play a song for you"\n```\n\n## Links\n\n- For more information [Read the docs](https://danialkeimasi.github.io/python-registerer/).\n\n## Installation\n\nYou can install the latest version of registerer from PyPI:\n\n```sh\npip install registerer\n```\n\n## Features\n\n- It\'s completely type-safe, thus you will get suggestions from your IDE.\n- Writing custom validations for registered items is provided without any inheritance.\n- generate choices for Django from registered items.\n- And so on...\n',
    'author': 'Danial Keimasi',
    'author_email': 'danialkeimasi@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/danialkeimasi/python-registerer',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
