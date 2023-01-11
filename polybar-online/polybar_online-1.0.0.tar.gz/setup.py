# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['polybar_online', 'polybar_online.status_printer', 'polybar_online.utils']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['polybar-online = polybar_online.main:main']}

setup_kwargs = {
    'name': 'polybar-online',
    'version': '1.0.0',
    'description': 'Script for Polybar that checks connection to the Internet',
    'long_description': "# Polybar Online\n\n**Polybar Online** is a script for Polybar that displays an internet connection indicator\nin a\npanel with the ability to send a notification when the connection is broken and restored.\n\n## Why another one?\n\nI've been looking for a similar module for myself and even found a couple. But they didn't\nrun on my machine... So I decided that it would be faster to write my own than to poke\naround in someone else's. (and others are not able to send notifications!!!)\n\n## Requirements\n\nThe script does not use any third-party libraries, but you will need to install some\n[Nerd fonts](https://github.com/ryanoasis/nerd-fonts) in order for the icons to be displayed.\n\nIt's not necessary if you're going to use your own icons from other fonts, though.\n\n## Installing\n\nClone the repository to a convenient location. For example, in `~/.config/polybar/`:\n\n```shell\ncd ~/.config/polybar/\ngit clone https://github.com/Leetovskiy/polybar-online \n```\n\nYou can also install Polybar Online from PyPI using `pip`. In this case, you may want to\nrun the script as a regular console program. To do this, make sure that the directory of\ninstalled pip packages is available in the `PATH` variable.\n\n```shell\npip install polybar-online\n```\n\n## Configuration\n\nThe script takes some arguments from the terminal to control its operation. These are, for\nexample, enabling and disabling Internet connection status change notifications, setting\nicons, etc.\n\nUse the command `polybar-online -h` to see the full list of available options.\n\n```\n  -h, --help            show this help message and exit\n  -n, --notify, --no-notify\n                        send a notification if the internet connection is broken (default: False)\n  --online-icon ONLINE_ICON\n                        icon that will be displayed when the Internet connection is available (default: 度)\n  --offline-icon OFFLINE_ICON\n                        icon that will be displayed when there is no Internet connection (default: ﴹ)\n  -ci CHECK_INTERVAL, --check-interval CHECK_INTERVAL\n                        Interval between checks (in seconds)\n  -ri RETRY_INTERVAL, --retry-interval RETRY_INTERVAL\n                        Interval between checks when Internet connection is unavailable (in seconds)\n```\n\n## Using\n\nYou need to put the script path in a special `custom/script` section of your Polybar\nconfiguration file. You also need the tail parameter set to true. And don't forget to add\nthe new module to your panel's module list.\n\nExample:\n\n```ini\n[bar/mybar]\nmodules-right = online\n\n[module/online]\ntype = custom/script\nexec = python ~/.config/polybar/polybar-online/polybar_online/main.py --notify -ci 5\ntail = true\n```\n\n## License\n\nThis little project is licensed under the Apache 2.0 license, so you are free to use it\naccording to the terms of the license.\n\n## Contribution\n\nIf you know how to improve this project or would like to contribute yourself, you are\nwelcome. I'm open to suggestions on Telegram ([@leetovskiy](https:/t.me/leetovskiy)) and\nemail ([dev.zaitsev@gmail.com](mailto:dev.zaitsev@gmail.com)), and I'll consider pull\nrequests from you as well.\n\n## Roadmap\n\n- [ ] Localization in Russian and other languages\n- [ ] Distribution as a binary (using nuitka)\n- [ ] AUR package",
    'author': 'Vitaliy Zaitsev',
    'author_email': 'dev.zaitsev@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Leetovskiy/polybar-online',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
