# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['inspector', 'inspector.windows']

package_data = \
{'': ['*'], 'inspector': ['static/*', 'static/assets/fonts/*']}

install_requires = \
['clr-loader==0.1.7',
 'importlib-metadata==4.13.0',
 'mss==6.1.0',
 'psutil==5.9.4',
 'pynput-robocorp-fork==5.0.0',
 'pythonnet==3.0.0a2',
 'pywebview==3.7.2',
 'requests==2.28.1',
 'robocorp-inspector-commons==0.6.6',
 'rpaframework-core==10.0.5',
 'rpaframework-recognition==5.0.1',
 'tk-tools==0.16.0',
 'typing-extensions==4.4.0']

extras_require = \
{':python_full_version != "3.7.6" and python_full_version != "3.8.1" and sys_platform == "win32"': ['pywin32>=302,<304'],
 ':sys_platform == "win32"': ['uiautomation==2.0.16']}

entry_points = \
{'console_scripts': ['inspector = inspector.cli:run']}

setup_kwargs = {
    'name': 'robocorp-inspector',
    'version': '0.8.5',
    'description': 'Robocorp Inspector',
    'long_description': '# Robocorp Inspector\n\nRobocorp Inspector is a tool for exploring various user interfaces\nand developing ways to target elements within them. An expression\nthat can target specific UI elemements is called a _locator_, and\nthese locators can be used to automate applications typically\nused by humans.\n\n## Dependencies\n\nYou might need to create a `.npmrc` file at project level with contents similar to the following, but with your own `authToken`.\nThis is needed for private repositories.\n\n```\nregistry=https://registry.npmjs.org/\n@robocorp:registry=https://npm.pkg.github.com/\n//npm.pkg.github.com/:_authToken=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n```\n\n> There is a hard dependency to the [Inspector Commons](https://github.com/robocorp/inspector-commons) implementation.\n> Most of the implementation resides in `inspector-commons` and if you spot any misalignment then you should correct it\n\n## Development\n\nThe project uses `invoke` for overall project management, `poetry` for\npython dependencies and environments, and `yarn` for Javascript dependencies\nand building.\n\nBoth `invoke` and `poetry` should be installed via pip: `pip install poetry invoke`\n\n- To see all possible tasks: `invoke --list`\n- To run the project: `invoke run `\n- For a quick build and run you can try running: `inv build-js && inv build && inv run`\n- To clean the dev environment you can use `inv clean` or `inv clean --force`\n\nAll source code is hosted on [GitHub](https://github.com/robocorp/inspector/).\n\n### Python & NPM\n\nTo launch the development environment you\'ll need:\n```\npyenv + virtualenv -> these will help building a dedicated python virtual environment\nnvm -> will help with a contained version of node + npm\n```\n\nIn order for everything to install and build properly use the following versions:\n```\npython -> v3.8.10\nnode -> v16.14.2\nnpm -> 8.5.0\n```\n\n## Usage\n\nRobocorp Inspector is distributed as a Python package with all front-end\ncomponents compiled and included statically.\n\nIf the package (and all required dependencies) is installed manually,\nit can be run with the command: `inspector`.\n\n## Code Organization\n\n> Attention: these might change over time & hopefully they will be maintained.\n\n### Inspector Class Diagram\n\n- not extremely precise\n- created to show how things link together from local implementation to `inspector-commons`\n\n![Inspector Class Diagram](./assets/InspectorClassDiagram.jpg)\n\n---\n\n<p align="center">\n  <img height="100" src="https://cdn.robocorp.com/brand/Logo/Dark%20logo%20transparent%20with%20buffer%20space/Dark%20logo%20transparent%20with%20buffer%20space.svg">\n</p>\n',
    'author': 'Ossi Rajuvaara',
    'author_email': 'ossi@rajuvaara.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/robocorp/inspector',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
