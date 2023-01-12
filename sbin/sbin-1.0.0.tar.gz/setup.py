# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bin',
 'bin.bin_file',
 'bin.bin_file.dtos',
 'bin.commands',
 'bin.commands.internal',
 'bin.custom_commands',
 'bin.custom_commands.dtos',
 'bin.env',
 'bin.models',
 'bin.process',
 'bin.process.io',
 'bin.requirements',
 'bin.requirements.dtos',
 'bin.up',
 'bin.up.dtos',
 'bin.version',
 'bin.virtualenv',
 'bin.virtualenv.dtos']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'colorama>=0.4.5,<0.5.0',
 'pydantic>=1.10.1,<2.0.0',
 'semantic-version>=2.10.0,<3.0.0']

entry_points = \
{'console_scripts': ['bin = bin.main:main', 'sbin = bin.main:main']}

setup_kwargs = {
    'name': 'sbin',
    'version': '1.0.0',
    'description': 'Makes your repo setup clean',
    'long_description': '# sbin\n\n[![versions](https://img.shields.io/pypi/pyversions/sbin.svg)](https://gitlab.com/mazmrini/bin)\n[![license](https://img.shields.io/gitlab/license/mazmrini/bin)](https://gitlab.com/mazmrini/bin/-/blob/main/LICENSE)\n\nAutomate your project setup with a simple `bin.yml` file.\n\n## Help\nSee [documentation](https://google.com) for more details.\n\n## Installation\nWe recommend installing `sbin` globally through `pip install sbin`.\n`sbin` and its alias `bin` executables will be available from the command line.\n\nPlease note that the documentation will refer to `sbin` as `bin`.\n\n## Quick start\nStart by creating an example `bin.yaml` file at the root of your project with\n```\nbin init\n```\n\nYou can explore bin commands through `bin <help|h|-h|--help>`. Here\nare some built-in ones:\n```\nbin req   # makes sure you have the requirements to run the projet \nbin up    # sets up whatever is needed to run the project\nbin down  # tear down whatever was up\n```\n\n## Examples\nHere are few project [examples](https://gitlab.com/mazmrini/bin/-/blob/main/examples) utilizing `bin`.\n\n## Contributing\nSee the [contributing](https://gitlab.com/mazmrini/bin/-/blob/main/CONTRIBUTING.md) doc.\n',
    'author': 'Mazine Mrini',
    'author_email': 'mazmrini@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/mazmrini/bin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
