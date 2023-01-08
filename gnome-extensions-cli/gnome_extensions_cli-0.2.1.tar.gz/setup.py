# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gnome_extensions_cli']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.5,<0.5.0']

entry_points = \
{'console_scripts': ['gnome-extensions-cli = gnome_extensions_cli.cli:run']}

setup_kwargs = {
    'name': 'gnome-extensions-cli',
    'version': '0.2.1',
    'description': 'Command line tool to manage your Gnome Shell extensions',
    'long_description': '![Github](https://img.shields.io/github/tag/essembeh/gnome-extensions-cli.svg)\n![PyPi](https://img.shields.io/pypi/v/gnome-extensions-cli.svg)\n![Python](https://img.shields.io/pypi/pyversions/gnome-extensions-cli.svg)\n![CI](https://github.com/essembeh/gnome-extensions-cli/actions/workflows/poetry.yml/badge.svg)\n\n# gnome-extensions-cli\n\nInstall, update and manage your Gnome Shell extensions from your terminal\n\n# Features\n\n- You can install any extension available on [Gnome website](https://extensions.gnome.org)\n- Use _DBus_ to communicate with _Gnome Shell_ like the Firefox addon does\n  - Also support non-DBus installations if needed\n- Automatically select the compatible version to install for your Gnome Shell\n- Automatic Gnome Shell restart if needed\n- Update all your extensions with one command: `gnome-extensions-cli update`\n- You can also uninstall, enable and disable extensions and open preferences\n\n# Install\n\nInstall from [PyPI](https://pypi.org/project/gnome-extensions-cli/)\n\n```sh\n$ pip3 install -u gnome-extensions-cli\n```\n\nInstall latest version from the repository\n\n```sh\n$ pip3 install -u git+https://github.com/essembeh/gnome-extensions-cli\n```\n\nOr setup a development environment\n\n```sh\n# dependencies to install PyGObject with pip\n$ sudo apt install libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-3.0\n\n# clone the repository\n$ git clone https://github.com/essembeh/gnome-extensions-cli\n$ cd gnome-extensions-cli\n\n# create the venv using poetry\n$ poetry install\n$ poetry shell\n(venv) $ gnome-extensions-cli --help\n```\n\n# Using\n\n## List your extensions\n\n```sh\n$ gnome-extensions-cli list\nInstalled extensions:\n[ ] auto-move-windows@gnome-shell-extensions.gcampax.github.com\n[X] dash-to-panel@jderose9.github.com (v37)\n[X] todo.txt@bart.libert.gmail.com (v25)\n\n# Use verbose to see available updates\n$ gnome-extensions-cli list -v\nInstalled extensions:\n[ ] auto-move-windows@gnome-shell-extensions.gcampax.github.com\n      available version: 37\n[X] dash-to-panel@jderose9.github.com (v37)\n[X] todo.txt@bart.libert.gmail.com (v25)\n```\n\n> Note: the first `[X]` or `[ ]` indicates if the extension is enabled or not\n\nYou also have a `search` command to print informations from Gnome extensions website\n\n```sh\n$ gnome-extensions-cli search 570\nTodo.txt: todo.txt@bart.libert.gmail.com\n    url: https://extensions.gnome.org/extension/570\n    tag: 8141\n    recommended version: 25\n    installed version: 25\n    available versions:\n      version 30 for Gnome Shell 3.36\n      version 29 for Gnome Shell 3.34\n      version 28 for Gnome Shell 3.32\n      [...]\n```\n\n## Install, uninstall and update\n\n```sh\n# Install extension by its UUID\n$ gnome-extensions-cli install dash-to-panel@jderose9.github.com\n\n# or use its package number from https://extensions.gnome.org\n$ gnome-extensions-cli install 1160\n\n# You can also install multiple extensions at once\n$ gnome-extensions-cli install 1160 570\n\n# Uninstall extensions\n$ gnome-extensions-cli uninstall todo.txt@bart.libert.gmail.com\n# ... or use extension number\n$ gnome-extensions-cli uninstall 570\n\n# You can enable and disable extensions\n$ gnome-extensions-cli disable todo.txt@bart.libert.gmail.com dash-to-panel@jderose9.github.com\n$ gnome-extensions-cli enable todo.txt@bart.libert.gmail.com\n# equivalent to\n$ gnome-extensions-cli disable 570 1160\n$ gnome-extensions-cli enable 570\n```\n\nThe `update` command by default updates only the _enabled_ extensions, use `--all/-a` to also update disabled extensions\n\n```sh\n# Update all enabled extensions\n$ gnome-extensions-cli update\n\n# Update only given extensions\n$ gnome-extensions-cli update dash-to-panel@jderose9.github.com\n# ... or use extension number\n$ gnome-extensions-cli update 1160\n```\n\n## Backends: DBus vs File\n\n`gnome-extensions-cli` can interact with Gnome Shell using two different implementations, using `dbus` or using a `file` based way:\n\n> By default, it uses `dbus` which is the safest way ;)\n\n### DBus\n\nUsing `--backend dbus`, the application uses _dbus_ messages to communicate with Gnome Shell directly.\n\nPros:\n\n- You are using the exact same way to install extensions as the Firefox addon\n- Automatically restart the Gnome Shell when needed\n- Very stable\n- You can open the extension preference dialog with `gnome-extensions-cli edit EXTENSION1_UUID`\n  Cons:\n- Installations are interactive, you are prompted with e Gnome Yes/No dialog before installing the extensions, so you need to have a running Gnome sessions\n\n### File\n\nUsing `--backend dbus`, the application uses unzip packages from [Gnome website](https://extensions.gnome.org) directly in you `~/.local/share/gnome-shell/extensions/` folder, enable/disable them and restarting the Gnome Shell using subprocesses.\n\nPros:\n\n- You can install extensions without any Gnome session running\n- Many `gnome-extensions-cli` alternatives use this method ... but\n  Cons:\n- Some extensions are not installed well\n',
    'author': 'Sébastien MB',
    'author_email': 'seb@essembeh.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/essembeh/gnome-extensions-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
