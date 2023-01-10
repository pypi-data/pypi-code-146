# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iotree', 'iotree.cli', 'iotree.core', 'iotree.utils']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.22.0,<0.23.0',
 'pytest>=7.2.0,<8.0.0',
 'pyyaml>=6.0,<7.0',
 'rich>=10.11.0,<13.0.0',
 'toml>=0.10.2,<0.11.0',
 'typer[all]>=0.7.0,<0.8.0',
 'xmltodict>=0.13.0,<0.14.0']

entry_points = \
{'console_scripts': ['iotree = iotree.cli:app']}

setup_kwargs = {
    'name': 'iotree',
    'version': '0.1.1',
    'description': 'A lightweight CLI + lib that allows you to perform basic IO tasks and display your content as rich trees and tables.',
    'long_description': '# A many-in-one tool for managing your Markup Language files.\n\n## What is it?\n\n**iotre** is a tool for managing your Markup Language files. It is capable to write and read files in the following formats:\n\n- JSON\n- YAML\n- TOML\n- XML\n- And soon more... :wink:\n\nThe basic goal was to have a small package anyone could add to their project and use it to manage their files. It is also possible to use it as a CLI tool.\n\n## Installation\n\nYou cannot install the CLI tool separately for now. You can install it with the following command:\n\n```bash\npip install iotree\n```\n\n## Usage\n\n### As a CLI tool\n\nTo see what the display function can do, you can use the following command:\n\n```bash\niotree demo\n```\n\nFor example, the following JSON file (displayed in VSCode)\n\n![JSON file](https://i.imgur.com/N4iKgMJ.png)\n\nwill be displayed like this:\n\n![JSON file displayed](https://i.imgur.com/tUSyW3L.png)\n\nWhile the following YAML file (displayed in VSCode)\n\n![YAML file](https://i.imgur.com/UE4ZxuQ.png)\n\nwill be displayed like this:\n\n![YAML file displayed](https://i.imgur.com/t3q5yHS.png)\n\n**Note**: The CLI tool is not yet finished. It is still in development.  \nIf this just looks like a wrapper around [rich trees](https://rich.readthedocs.io/en/stable/tree.html)) to you, it almost because it is. :wink:\n\nAs a CLI tool, the key difference I want to bring is the ability to configure *themes* and *styles*.\n\nJust run the following command to interactively create a theme:\n\n```bash\niotree config init\n```\n\nBut if you\'re lazy, just use a file:\n\n```bash\niotree config init from-json my_theme.json\n```\n\nFor example, the following JSON file\n\n```json\n{   \n    "name": "My super pseudonym",\n    "username": "my.username",\n    "symbol": "lgpoint",\n    "theme": "bright-blue-green"\n}\n```\n\nwill result in the following theme: ... \n',
    'author': 'Arno V',
    'author_email': 'bcda0276@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
