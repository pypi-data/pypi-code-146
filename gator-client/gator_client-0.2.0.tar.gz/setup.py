# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gator', 'gator.api.client']

package_data = \
{'': ['*']}

install_requires = \
['certifi>=2022.6.15,<2023.0.0',
 'gator-core>=1.1.4,<2.0.0',
 'urllib3>=1.26.9,<2.0.0']

setup_kwargs = {
    'name': 'gator-client',
    'version': '0.2.0',
    'description': 'A web client for the Gator API',
    'long_description': '# Gator Client\nA web client for the [Gator](https://github.com/sqrl-planner/gator) API.\n\n## Package manager\ngator-client uses the [poetry](https://python-poetry.org/) package manager to manage its dependencies. To install the dependencies, run the following command:\n```\npoetry install\n```\nSee the [poetry](https://python-poetry.org/) documentation for more information and\ninstallation instructions.\n\n<!-- ... Insert content here ... -->\n\n## Tools\n\nThere are a number of tools available to help you with the development of sqrl. These tools ensure that your code is well-formed, follows the best practices, and\nis consistent with the rest of the project.\n\n#### Linting the codebase\n- For detecting code quality and style issues, run ``flake8``\n- For checking compliance with Python docstring conventions, run ``pydocstyle``\n\n**NOTE**: these tools will not fix any issues, but they can help you identify potential problems.\n\n#### Formatting the codebase\n- For automatically formatting the codebase, run ``autopep8 --in-place --recursive .``. For more information on this command, see the [autopep8](https://pypi.python.org/pypi/autopep8) documentation.\n- For automatically sorting imports, run ``isort .``\n\n#### Running tests\nFor running tests, run ``pytest``.\n',
    'author': 'Shon Verch',
    'author_email': 'verchshon@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
