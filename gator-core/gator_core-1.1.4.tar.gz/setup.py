# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gator',
 'gator.core.data',
 'gator.core.data.providers',
 'gator.core.data.providers.uoft',
 'gator.core.data.utils',
 'gator.core.models',
 'gator.core.schemas']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'marshmallow-enum>=1.5.1,<2.0.0',
 'marshmallow>=3.17.0,<4.0.0',
 'mongoengine>=0.20',
 'requests>=2.28.2,<3.0.0',
 'routes>=2.5.1,<3.0.0']

setup_kwargs = {
    'name': 'gator-core',
    'version': '1.1.4',
    'description': 'A dataset aggregation framework for Sqrl Planner.',
    'long_description': '# gator-core\n A dataset aggregation framework for Sqrl Planner.\n\n## Tools\n\n#### Linting the codebase\nFor detecting code quality and style issues, run\n```\nflake8\n```\nFor checking compliance with Python docstring conventions, run\n```\npydocstyle\n```\n\n**NOTE**: these tools will not fix any issues, but they can help you identify potential problems.\n\n\n#### Formatting the codebase\nFor automatically formatting the codebase, run\n```\nautopep8 --in-place --recursive .\n```\nFor more information on this command, see the [autopep8](https://pypi.python.org/pypi/autopep8) documentation.\n\nFor automatically sorting imports, run\n```\nisort .\n```\n',
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
