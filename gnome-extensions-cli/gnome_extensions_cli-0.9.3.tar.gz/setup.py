# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gnome_extensions_cli', 'gnome_extensions_cli.commands']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.5,<0.5.0',
 'more-itertools>=9.0.0,<10.0.0',
 'packaging>=23.0,<24.0',
 'pydantic>=1.10.4,<2.0.0',
 'requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['gext = gnome_extensions_cli.cli:run',
                     'gnome-extensions-cli = gnome_extensions_cli.cli:run']}

setup_kwargs = {
    'name': 'gnome-extensions-cli',
    'version': '0.9.3',
    'description': 'Command line tool to manage your Gnome Shell extensions',
    'long_description': "![Github](https://img.shields.io/github/tag/essembeh/gnome-extensions-cli.svg)\n![PyPi](https://img.shields.io/pypi/v/gnome-extensions-cli.svg)\n![Python](https://img.shields.io/pypi/pyversions/gnome-extensions-cli.svg)\n![CI](https://github.com/essembeh/gnome-extensions-cli/actions/workflows/poetry.yml/badge.svg)\n\n# gnome-extensions-cli\n\nInstall, update and manage your Gnome Shell extensions from your terminal !\n\n# Features\n\n- You can install any extension available on [Gnome website](https://extensions.gnome.org)\n- Use _DBus_ to communicate with _Gnome Shell_ like the Firefox addon does\n  - Also support non-DBus installations if needed\n- Automatically select the compatible version to install for your Gnome Shell\n- Update all your extensions with one command: `gext update`\n\nAvailable commands:\n\n- `gext list` to list you installed extensions\n- `gext search` to search for extensions on [Gnome website](https://extensions.gnome.org)\n- `gext install` to install extensions\n- `gext install` to update any or all your extensions\n- `gext uninstall` to uninstall extensions\n- `gext show` to show details about extensions\n- `gext enable` to enable extensions\n- `gext disable` to disable extensions\n- `gext preferences` to open the extension configuration window\n\n> Note: `gext` is an alias of `gnome-extensions-cli`\n\n# Install\n\n## Releases\n\nReleases are available on [PyPI](https://pypi.org/project/gnome-extensions-cli/)\n\n> Note: [PipX](https://pypi.org/project/pipx/) is the recommended way to install 3rd-party apps in dedicated environments.\n\n```sh\n# install using pip\n$ pip3 install --upgrade gnome-extensions-cli\n\n# or using pipx (you need to install pipx first)\n$ pipx install gnome-extensions-cli --system-site-packages\n\n# gext is an alias for gnome-extensions-cli\n$ gnome-extensions-cli --help\n$ gext --help\n```\n\n## From the source\n\nYou can also install the _latest_ version from the Git repository:\n\n```sh\n$ pip3 install --upgrade git+https://github.com/essembeh/gnome-extensions-cli\n```\n\nYou can setup a development environment with, requires [Poetry](https://python-poetry.org/)\n\n```sh\n# dependencies to install PyGObject with pip\n$ sudo apt install libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-3.0\n\n# clone the repository\n$ git clone https://github.com/essembeh/gnome-extensions-cli\n$ cd gnome-extensions-cli\n\n# install poetry if you don't have it yet\n$ pipx install poetry\n\n# create the venv using poetry\n$ poetry install\n$ poetry shell\n(.venv) $ gnome-extensions-cli --help\n```\n\n# Using\n\n## List your extensions\n\nBy default, the `list` command only display the _enabled_ extensions, using `-a|--all` argument also displays _disabled_ ones.\n\n![gext list](images/list.png)\n\n## Install, update or uninstall extensions\n\nThe `install` commands allows you to install extensions from their _uuid_ or _pk_.\n\n> Note: You can use `search` command to find extensions, `gext` prints _uuids_ in _yellow_ .\n\n```sh\n# Install extension by its UUID\n$ gext install dash-to-panel@jderose9.github.com\n\n# or use its package number from https://extensions.gnome.org\n$ gext install 1160\n\n# You can also install multiple extensions at once\n$ gext install 1160 todo.txt@bart.libert.gmail.com\n\n# Uninstall extensions\n$ gext uninstall todo.txt@bart.libert.gmail.com\n\n# You can enable and disable extensions\n$ gext enable todo.txt@bart.libert.gmail.com\n$ gext disable todo.txt@bart.libert.gmail.com dash-to-panel@jderose9.github.com\n```\n\n![gext install](images/install.gif)\n\nThe `update` command without arguments updates all _enabled_ extensions.\nYou can also `update` a specific extension by giving its _uuid_.\n\n![gext update](images/update.gif)\n\n> Note: the `--install` argument allow you to _install_ extensions given to `update` command if they are not installed.\n\n## Search for extensions and show details\n\nThe `search` command searches from [Gnome website](https://extensions.gnome.org) and prints results in your terminal:\n\n![gext search](images/search.png)\n\nThe `show` command fetches details from _Gnome website_ and prints them:\n\n![gext show](images/show.png)\n\n# Under the hood: DBus vs Filesystem\n\n`gext` can interact with Gnome Shell using two different implementations, using `dbus` or using a `filesystem` operations.\n\n> Note: By default, it uses `dbus` (as it is the official way), but switches to `filesystem` if `dbus` is not available (like with _ssh_ sessions)\n\n## DBus\n\nUsing `--dbus`, the application uses _dbus_ messages with DBus Python API to communicate with Gnome Shell directly.\n\nInstallations are interactive, like when you install extensions from your brower on Gnome website, you are prompted with a Gnome _Yes/No_ dialog before installing the extensions\n\nPros:\n\n- You are using the exact same way to install extensions as the Firefox addon\n- Automatically restart the Gnome Shell when needed\n- Very stable\n- You can open the extension preference dialog with `gext edit EXTENSION_UUID`\n\nCons:\n\n- You need to have a running Gnome session\n\n## Filesystem backend\n\nUsing `--filesystem`, the application uses unzip packages from [Gnome website](https://extensions.gnome.org) directly in you `~/.local/share/gnome-shell/extensions/` folder, enable/disable them and restarting the Gnome Shell using subprocesses.\n\nPros:\n\n- You can install extensions without any Gnome session running (usign _ssh_ for example)\n- Many `gext` alternatives CLI tools use this method\n\nCons:\n\n- Some extensions might not install well\n",
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
