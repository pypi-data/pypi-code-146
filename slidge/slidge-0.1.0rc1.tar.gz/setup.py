# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slidge',
 'slidge.core',
 'slidge.core.mixins',
 'slidge.core.muc',
 'slidge.plugins',
 'slidge.plugins.discord',
 'slidge.plugins.mattermost',
 'slidge.plugins.signal',
 'slidge.plugins.telegram',
 'slidge.plugins.whatsapp',
 'slidge.util',
 'slidge.util.xep_0030',
 'slidge.util.xep_0030.stanza',
 'slidge.util.xep_0050',
 'slidge.util.xep_0077',
 'slidge.util.xep_0100',
 'slidge.util.xep_0292',
 'slidge.util.xep_0356',
 'slidge.util.xep_0356_old',
 'slidge.util.xep_0461']

package_data = \
{'': ['*']}

install_requires = \
['ConfigArgParse>=1.5.3,<2.0.0',
 'Pillow>=8.1.0',
 'aiohttp>=3.6.0',
 'pickle-secure>=0.9.99,<0.10.0',
 'qrcode>=7.3',
 'slixmpp>=1.8.3,<2.0.0']

extras_require = \
{'discord': ['discord.py-self>=1.9.2,<2.0.0'],
 'facebook': ['mautrix-facebook>=0.4.1,<0.5.0'],
 'mattermost': ['mattermost-api-reference-client>=4.0.0,<5.0.0',
                'emoji>=2.0.0,<3.0.0'],
 'signal': ['aiosignald>=0.3.4,<0.4.0'],
 'skype': ['SkPy>=0.10.4,<0.11.0'],
 'steam': ['steam[client]>=1.3.0,<2.0.0'],
 'telegram': ['aiotdlib>=0.19.2,<0.20.0', 'pydantic']}

entry_points = \
{'console_scripts': ['slidge = slidge.__main__:main']}

setup_kwargs = {
    'name': 'slidge',
    'version': '0.1.0rc1',
    'description': 'XMPP bridging framework',
    'long_description': 'Slidge 🛷\n========\n\n[Home](https://sr.ht/~nicoco/slidge) |\n[Source](https://sr.ht/~nicoco/slidge/sources) |\n[Issues](https://sr.ht/~nicoco/slidge/trackers) |\n[Patches](https://lists.sr.ht/~nicoco/public-inbox) |\n[Chat](xmpp:slidge@conference.nicoco.fr?join)\n\nTurn any XMPP client into that fancy multiprotocol chat app that every cool kid want.\n\n[![Documentation status](https://readthedocs.org/projects/slidge/badge/?version=latest)](https://slidge.readthedocs.io/)\n[![builds.sr.ht status](https://builds.sr.ht/~nicoco/slidge/commits/master/ci.yml.svg)](https://builds.sr.ht/~nicoco/slidge/commits/master/ci.yml?)\n[![Debian package](https://builds.sr.ht/~nicoco/slidge/commits/master/debian.yml.svg)](https://builds.sr.ht/~nicoco/slidge/commits/master/debian.yml?)\n[![pypi](https://badge.fury.io/py/slidge.svg)](https://pypi.org/project/slidge/)\n\nSlidge is a general purpose XMPP (puppeteer) gateway framework in python.\nIt\'s a work in progress, but it should make\n[writing gateways to other chat networks](https://slidge.readthedocs.io/en/latest/dev/tutorial.html)\n(*plugins*) as frictionless as possible.\n\nIt comes with a few plugins included, implementing at least basic direct messaging and often more "advanced"\ninstant messaging features:\n\n|            | Presences[¹] | Typing[²] | Marks[³] | Upload[⁴] | Edit[⁵] | React[⁶] | Retract[⁷] | Reply[⁸] | Groups[⁹] |\n|------------|--------------|-----------|----------|-----------|---------|----------|------------|----------|-----------|\n| Signal     | N/A          | ✅        | ✅       | ✅        | N/A     | ✅       | ✅         | ✅       | ~         |\n| Telegram   | ✅           | ✅        | ✅       | ✅        | ✅      | ✅       | ✅         | ✅       | ~         |\n| Discord    | ❌           | ✅        | N/A      | ✅        | ✅      | ~        | ✅         | ✅       | ❌         |\n| Steam      | ✅           | ✅        | N/A      | ❌        | N/A     | ~        | N/A        | N/A      | ❌         |\n| Mattermost | ✅           | ✅        | ~        | ✅        | ✅      | ✅       | ✅         | ❌       | ❌         |\n| Facebook   | ❌           | ✅        | ✅       | ✅        | ✅      | ✅       | ✅         | ✅       | ❌         |\n| Skype      | ✅           | ✅        | ❌       | ✅        | ✅      | ❌       | ✅         | ❌       | ❌         |\n| WhatsApp   | ✅           | ✅        | ✅       | ✅        | N/A     | ✅       | ✅         | ✅       | ❌         |\n\n\n[¹]: https://xmpp.org/rfcs/rfc6121.html#presence\n[²]: https://xmpp.org/extensions/xep-0085.html\n[³]: https://xmpp.org/extensions/xep-0333.html\n[⁴]: https://xmpp.org/extensions/xep-0363.html\n[⁵]: https://xmpp.org/extensions/xep-0308.html\n[⁶]: https://xmpp.org/extensions/xep-0444.html\n[⁷]: https://xmpp.org/extensions/xep-0424.html\n[⁸]: https://xmpp.org/extensions/xep-0461.html\n[⁹]: https://xmpp.org/extensions/xep-0045.html\n\n\nThis table may not be entirely accurate, but **in theory**, stuff marked ✅ works.\nN/A means that the legacy network does not have an equivalent of this XMPP feature\n(because XMPP is better, what did you think?).\n\n**WARNING**: you may break the terms of use of a legacy network and end up getting your account locked\nby using slidge. Refer to the\n[keeping a low profile](https://slidge.readthedocs.io/en/latest/user/low_profile.html)\ndocumentation page for more info.\n\nStatus\n------\n\nSlidge is **beta**-grade software for 1:1 chats.\nGroup chat support is **experimental**.\n\nTry slidge and give us some\nfeedback, through the [MUC](xmpp:slidge@conference.nicoco.fr?join), the\n[issue tracker](https://todo.sr.ht/~nicoco/slidge) or in the\n[public inbox](https://lists.sr.ht/~nicoco/public-inbox).\nDon\'t be shy!\n\nInstallation\n------------\n\n### containers\n\nContainers for arm64 and amd64 are available on\n[docker hub](https://hub.docker.com/u/nicocool84).\n\n### debian\n\nDebian packages for *bullseye* (amd64 only for now, help welcome\nto support other architectures)\nare built on each push to master as artifacts of\n[this build job](https://builds.sr.ht/~nicoco/slidge/commits/master/debian.yml?).\n\nA repo is maintained by IGImonster. To use it do this (as root):\n\n```sh\n# trust the repo\'s key\nwget -O- http://deb.slidge.im/repo/slidge.gpg.key \\\n  |gpg --dearmor \\\n  |tee /usr/share/keyrings/slidge.gpg > /dev/null\n# add the repo, replace \'release\' with \'nightly\' if you\'re feeling adventurous \necho "deb [signed-by=/usr/share/keyrings/slidge.gpg] http://deb.slidge.im/repo/debian release main" \\\n  > /etc/apt/sources.list.d/slidge.list\n# install\napt update && apt install slidge -y\n```\n\nRefer to [the docs](https://slidge.readthedocs.io/en/latest/admin/launch.html#debian-packages)\nfor information about how to use the provided systemd service files.\n\n### pip\n\nTagged releases are uploaded to [pypi](https://pypi.org/project/slidge/).\n\n```sh\npip install slidge[signal]  # you can replace signal with any network listed in the table above\npython -m slidge --legacy-module=slidge.plugins.signal\n```\n\nIf you\'re looking for the bleeding edge, download an artifact\n[here](https://builds.sr.ht/~nicoco/slidge/commits/master/ci.yml?).\n\nAbout privacy\n-------------\n\nSlidge (and most if not all XMPP gateway that I know of) will break\nend-to-end encryption, or more precisely one of the \'ends\' become the\ngateway itself. If privacy is a major concern for you, my advice would\nbe to:\n\n-   use XMPP + OMEMO\n-   self-host your gateways\n-   have your gateways hosted by someone you know AFK and trust\n\nRelated projects\n----------------\n\n-   [Spectrum](https://www.spectrum.im/)\n-   [Bitfrost](https://github.com/matrix-org/matrix-bifrost)\n-   [Mautrix](https://github.com/mautrix)\n-   [matterbridge](https://github.com/42wim/matterbridge)\n-   [XMPP-discord-bridge](https://git.polynom.me/PapaTutuWawa/xmpp-discord-bridge)\n',
    'author': 'Nicolas Cedilnik',
    'author_email': 'nicoco@nicoco.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://sr.ht/~nicoco/slidge/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
