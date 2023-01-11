# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['inspector_commons', 'inspector_commons.api', 'inspector_commons.bridge']

package_data = \
{'': ['*'], 'inspector_commons': ['static/resources/*']}

install_requires = \
['psutil==5.9.4',
 'requests==2.28.1',
 'rpaframework-core==10.0.5',
 'typing-extensions==4.4.0']

extras_require = \
{':python_full_version != "3.7.6" and python_full_version != "3.8.1" and sys_platform == "win32"': ['pywin32>=302,<304'],
 ':sys_platform == "win32"': ['pynput-robocorp-fork==5.0.0',
                              'uiautomation==2.0.16']}

setup_kwargs = {
    'name': 'robocorp-inspector-commons',
    'version': '0.6.6',
    'description': 'Robocorp Inspector Commons',
    'long_description': '# Robocorp Inspector Commons\n\nRobocorp Inspector Commons is the commons package for Robocorp Inspector.\n\n## Dependencies\n\nYou might need to create a `.npmrc` file at project level with contents similar to the following, but with your own `authToken`.\nThis is needed for private repositories.\n\n```\nregistry=https://registry.npmjs.org/\n@robocorp:registry=https://npm.pkg.github.com/\n//npm.pkg.github.com/:_authToken=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n```\n\n## Development\n\nThe project uses `invoke` for overall project management, `poetry` for\npython dependencies and environments, and `npm` for Javascript dependencies\nand building.\n\nBoth `invoke` and `poetry` should be installed via pip: `pip install poetry invoke`\n\n- To see all possible tasks: `invoke --list`\n\nAll source code is hosted on [GitHub](https://github.com/robocorp/inspector-commons/).\n\n## Usage\n\nRobocorp Inspector Commons is distributed as a Python package with all browser overlay\ncomponents compiled and included statically.\n\n### Link to Automation Studio and running with Automation Studio\n\n1. Terminal 1:\n   1. ***Automation Studio***: run `invoke build-dev`\n   2. ***Inspector-commons***: run `invoke linkas`\n   3. ***Inspector-commons***: run `invoke watch`\n2. Terminal 2:\n   1. ***Automation Studio/robotd***: run `invoke start`\n3. Terminal 3:\n   1. ***Automation Studio***: run `invoke start --port=<PORT robotd started in>`\n\n---\n\n<p align="center">\n  <img height="100" src="https://cdn.robocorp.com/brand/Logo/Dark%20logo%20transparent%20with%20buffer%20space/Dark%20logo%20transparent%20with%20buffer%20space.svg">\n</p>\n',
    'author': 'Robocorp',
    'author_email': 'dev@robocorp.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/robocorp/inspector',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
