# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['doorstop_edit',
 'doorstop_edit.dialogs',
 'doorstop_edit.item_edit',
 'doorstop_edit.item_render',
 'doorstop_edit.item_tree',
 'doorstop_edit.pinned_items',
 'doorstop_edit.ui_gen',
 'doorstop_edit.utils']

package_data = \
{'': ['*']}

install_requires = \
['PySide6>=6.4.0,<7.0.0',
 'doorstop>=2.2.post1',
 'markdown>=3.4.0,<4.0.0',
 'mdformat-myst>=0.1.5,<0.2.0',
 'plantuml-markdown>=3.8.0,<4.0.0',
 'pygments>=2.14.0,<3.0.0',
 'qt-material>=2.12,<3.0',
 'setuptools>=65.0.0,<66.0.0']

entry_points = \
{'console_scripts': ['doorstop-edit = doorstop_edit.main:main']}

setup_kwargs = {
    'name': 'doorstop-edit',
    'version': '0.1.0b5',
    'description': 'Cross-platform doorstop GUI editor',
    'long_description': "[![PyPI Version](https://img.shields.io/pypi/v/doorstop-edit.svg)](https://pypi.org/project/doorstop-edit)\n[![Linux Test](https://github.com/ownbee/doorstop-edit/actions/workflows/test.yml/badge.svg)](https://github.com/ownbee/doorstop-edit/actions/workflows/test.yml)\n[![Coverage Status](https://img.shields.io/codecov/c/gh/ownbee/doorstop-edit)](https://codecov.io/gh/ownbee/doorstop-edit)\n\n# Doorstop Edit\n\n_A cross-platform GUI editor for [Doorstop](https://github.com/doorstop-dev/doorstop) powered by PySide6 (Qt)._\n\nThe goal of this GUI is to provide all the tools needed to efficiently work with a larger set of\nrequirements within the editor and at the same time have full control of what is happening. The\neditor use the doorstop API whenever possible to behave the same way as doorstop.\n\n![Sample](https://raw.githubusercontent.com/ownbee/doorstop-edit/main/sample.png)\n\n**Features:**\n\n* **Resizable and movable modern views** for custom layout.\n* **Dark theme**.\n* Item tree with **status colors** and **search function** for good overview and fast location.\n* **Live markdown-HTML** rendering.\n* **Section or single mode** reading.\n* **Review** and **clear suspect links**.\n* Edit additional attributes with `boolean` and `string` types.\n* Built-in **item diff tool** to review changes made on disk.\n* **Markdown formatting tool** powered by `mdformat` for the text attribute.\n* **Pin feature** for easy access to work-in-progress items.\n* And more...\n\n\n**TODO list:**\n\n* Add and remove document.\n* Validating documents and items in a user-friendly manner.\n* File watcher for syncing/refreshing when changes made on disk.\n* Ability to change project root.\n\n## Install\n\nAutomatic install with pip:\n\n```sh\npip install doorstop-edit\n```\n\nFor source installation see *Contributing* section.\n\n## Demo/Testing\n\nThere is a python script that generates a document tree which can be useful when testing this\napplication.\n\n```sh\npython3 tools/gen_sample_tree.py\n\n# Output will be located in the dist/ folder.\n```\n\n\n## Other doorstop GUI's\n\nThere exists at least two well known GUI's for doorstop editing,\n[doorhole](https://github.com/sevendays/doorhole) and the build-in GUI in doorstop.\n\nSince both are pretty basic and have missing features when working with a large and complex set of\nrequrements, this new GUI was created to fill in some gaps.\n\n\n## Contributing\n\nSee [CONTRIBUTING.md](https://github.com/ownbee/doorstop-edit/blob/main/CONTRIBUTING.md).\n",
    'author': 'Alexander Ernfridsson',
    'author_email': 'ernfridsson@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ownbee/doorstop-edit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
