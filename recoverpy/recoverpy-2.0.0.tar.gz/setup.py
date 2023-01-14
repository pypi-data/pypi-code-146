# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['recoverpy',
 'recoverpy.lib',
 'recoverpy.lib.search',
 'recoverpy.models',
 'recoverpy.ui',
 'recoverpy.ui.css',
 'recoverpy.ui.screens',
 'recoverpy.ui.widgets']

package_data = \
{'': ['*']}

install_requires = \
['textual>=0.9.0,<0.10.0']

setup_kwargs = {
    'name': 'recoverpy',
    'version': '2.0.0',
    'description': 'A TUI to recover overwritten or deleted data.',
    'long_description': '<div align="center">\n    <img src="docs/assets/logo.png" alt="RecoverPy">\n</div>\n\n<p align="center">\n    <em>Recover overwritten or deleted data.</em>\n</p>\n\n<p align="center">\n<a href="https://img.shields.io/github/v/release/pablolec/recoverpy" target="_blank">\n    <img src="https://img.shields.io/github/v/release/pablolec/recoverpy" alt="Release">\n</a>\n<a href="https://github.com/PabloLec/recoverpy/blob/main/LICENSE" target="_blank">\n    <img src="https://img.shields.io/github/license/pablolec/recoverpy" alt="License">\n</a>\n<a href="https://pepy.tech/project/recoverpy" target="_blank">\n    <img src="https://static.pepy.tech/personalized-badge/recoverpy?period=total&units=abbreviation&left_color=grey&right_color=red&left_text=downloads" alt="Downloads">\n</a>\n\n<a href="#" target="_blank">\n    <img src="https://github.com/PabloLec/recoverpy/actions/workflows/pytest.yml/badge.svg?branch=main" alt="Tests">\n</a>\n</p>\n\n---\n\n<!--ts-->\n   * [Demo](#Demo)\n   * [Installation](#Installation)\n      * [Dependancies](#arrow_right-dependancies)\n      * [Installation from pip](#arrow_right-installation-from-pip)\n   * [Usage](#Usage)\n   * [Tips](#Tips)\n   * [Contributing](#Contributing)\n<!--te-->\n\n---\n\n# RecoverPy\n\nRecoverPy is a powerful tool that leverages your system capabilities to recover lost files.\n\nUnlike others, you can not only recover deleted files but also **overwritten** data.\n\nEvery block of your partition will be scanned. You can even find a string in binary files.\n## Demo\n\n<p align="center">\n    <img src="docs/assets/demo.gif">\n</p>\n\n## Installation\n\n:penguin: RecoverPy is currently only available on Linux systems.\n\n#### :arrow_right: Dependancies\n\n**Mandatory:** To list and search through your partitions, recoverpy uses `grep`, `dd`, and `lsblk` commands.\n\n**Optional:** To display real time grep progress, you can install `progress`.\n\nTo install all dependencies:\n- Debian-like: `apt install grep coreutils util-linux progress`\n- Arch: `pacman -S grep coreutils util-linux progress`\n- Fedora: `dnf install grep coreutils util-linux progress`\n\n#### :arrow_right: Installation from pip\n\n`python3 -m pip install recoverpy`\n\n## Usage\n\n```bash\npython3 -m recoverpy\n```\n\n:red_circle: **You must be root or use sudo**.\n\n:arrow_right: Default save path is `/tmp/`, click on Settings to edit configuration.\n\n---\n\n:one: **Select the system partition** in which your file was. If you are out of luck, you can alternatively search in your home partition, maybe your IDE, text editor, etc. made a backup at some point.\n\n:two: **Type a text string to search**. See tips below for better results.\n\n:three: **Start search**, Results will appear in the left-hand box.\n\n:four: **Select a result** to display the corresponding partition block content in the right-hand box.\n\n:five: Once you have found your precious, **select `Save`**.\n\n:six: You can now either save this block individually or explore neighboring blocks for the remaining parts of the file. You could then save it all in one file.\n\n## Tips\n\n- Always do backups! Yes, maybe too late...\n- **Unmount your partition before you do anything!** Although you can search with your partition still mounted, it is highly recommended to unmount your partition to avoid any alteration to your file.\n\nRegarding the searched string:\n\n- Be concise, find something that could be unique to your file.\n- Stay simple, your string is escaped but exotic characters may affect your results.\n- Try to remember the last edit you have made to your file.\n\nWhen you have found your file:\n\n- You might see multiple results. Your system often use different partion blocks to save successive versions of a file. Make sure you\'ve found the last version.\n- Use the option to explore neighboring blocks to make sure you do not miss some part of your file.\n\n## Contributing\n\nThank you for considering contributing to RecoverPy.\nAny request, bug report or PR are welcome. Please read the [contributing guide](CONTRIBUTING.md).\n',
    'author': 'PabloLec',
    'author_email': 'pablolec@pm.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/PabloLec/recoverpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
