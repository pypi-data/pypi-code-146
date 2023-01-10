# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gnome_extensions_cli', 'gnome_extensions_cli.commands']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.5,<0.5.0',
 'more-itertools>=9.0.0,<10.0.0',
 'pydantic>=1.10.4,<2.0.0',
 'requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['gext = gnome_extensions_cli.cli:run',
                     'gnome-extensions-cli = gnome_extensions_cli.cli:run']}

setup_kwargs = {
    'name': 'gnome-extensions-cli',
    'version': '0.9.0',
    'description': 'Command line tool to manage your Gnome Shell extensions',
    'long_description': '![Github](https://img.shields.io/github/tag/essembeh/gnome-extensions-cli.svg)\n![PyPi](https://img.shields.io/pypi/v/gnome-extensions-cli.svg)\n![Python](https://img.shields.io/pypi/pyversions/gnome-extensions-cli.svg)\n![CI](https://github.com/essembeh/gnome-extensions-cli/actions/workflows/poetry.yml/badge.svg)\n\n# gnome-extensions-cli\n\nInstall, update and manage your Gnome Shell extensions from your terminal\n\n# Features\n\n- You can install any extension available on [Gnome website](https://extensions.gnome.org)\n- Use _DBus_ to communicate with _Gnome Shell_ like the Firefox addon does\n  - Also support non-DBus installations if needed\n- Automatically select the compatible version to install for your Gnome Shell\n- Automatic Gnome Shell restart if needed\n- Update all your extensions with one command: `gnome-extensions-cli update`\n- You can also uninstall, enable or disable extensions and open preferences\n\n# Install\n\nInstall from [PyPI](https://pypi.org/project/gnome-extensions-cli/)\n\n```sh\n$ pip3 install -u gnome-extensions-cli\n```\n\nInstall latest version from the repository\n\n```sh\n$ pip3 install -u git+https://github.com/essembeh/gnome-extensions-cli\n```\n\nOr setup a development environment\n\n```sh\n# dependencies to install PyGObject with pip\n$ sudo apt install libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-3.0\n\n# clone the repository\n$ git clone https://github.com/essembeh/gnome-extensions-cli\n$ cd gnome-extensions-cli\n\n# create the venv using poetry\n$ poetry install\n$ poetry shell\n(venv) $ gnome-extensions-cli --help\n```\n\n# Using\n\n## List your extensions\n\nBy default, the `list` command only display the _enabled_ extensions, using `-a|--all` argument also displays _disabled_ ones.\n\n![gnome-extensions-cli list](images/list.png)\n\n## Show some details about extensions\n\nThe `show` command fetch details from _Gnome website_ and print them.s.\n\n![gnome-extensions-cli show](images/show.png)\n\n## Install, uninstall and update\n\n![gnome-extensions-cli install](images/install.gif)\n\n```sh\n# Install extension by its UUID\n$ gnome-extensions-cli install dash-to-panel@jderose9.github.com\n\n# or use its package number from https://extensions.gnome.org\n$ gnome-extensions-cli install 1160\n\n# You can also install multiple extensions at once\n$ gnome-extensions-cli install 1160 todo.txt@bart.libert.gmail.com\n\n# Uninstall extensions\n$ gnome-extensions-cli uninstall todo.txt@bart.libert.gmail.com\n\n# You can enable and disable extensions\n$ gnome-extensions-cli enable todo.txt@bart.libert.gmail.com\n$ gnome-extensions-cli disable todo.txt@bart.libert.gmail.com dash-to-panel@jderose9.github.com\n```\n\nThe `update` command without arguments updates all _enabled_ extensions.\nYou can also `update` a specific extension by giving its _uuid_.\n\n![gnome-extensions-cli update](images/update.gif)\n\n> Note: the `--install` argument allow you to _install_ extensions given to `update` command if they are not installed.\n\n## Backends: DBus vs Filesystem\n\n`gnome-extensions-cli` can interact with Gnome Shell using two different implementations, using `dbus` or using a `filesystem` operations:\n\n> Note: By default, it uses `dbus` (as it is the official way), but switches to `filesystem` if `dbus` is not available)\n\n### DBus backend\n\nUsing `--dbus`, the application uses _dbus_ messages to communicate with Gnome Shell directly.\n\nPros:\n\n- You are using the exact same way to install extensions as the Firefox addon\n- Automatically restart the Gnome Shell when needed\n- Very stable\n- You can open the extension preference dialog with `gnome-extensions-cli edit EXTENSION_UUID`\n\nCons:\n\n- Installations are interactive, you are prompted with a Gnome _Yes/No_ dialog before installing the extensions, so you need to have a running Gnome session\n\n### Filesystem backend\n\nUsing `--filesystem`, the application uses unzip packages from [Gnome website](https://extensions.gnome.org) directly in you `~/.local/share/gnome-shell/extensions/` folder, enable/disable them and restarting the Gnome Shell using subprocesses.\n\nPros:\n\n- You can install extensions without any Gnome session running (usign _ssh_ for example)\n- Many `gnome-extensions-cli` alternatives use this method ... but\n\nCons:\n\n- Some extensions are not installed well\n',
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
