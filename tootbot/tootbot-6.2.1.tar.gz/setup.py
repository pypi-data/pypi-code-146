# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tootbot']

package_data = \
{'': ['*']}

install_requires = \
['Brotli>=1.0.9,<2.0.0',
 'aiodns>=3.0.0,<4.0.0',
 'aiohttp>=3.8.1,<4.0.0',
 'aiosqlite>=0.17.0,<0.18.0',
 'arrow>=1.2.2,<2.0.0',
 'asyncpraw>=7.5.0,<8.0.0',
 'coloredlogs>=15.0.1,<16.0.0',
 'imgurpython>=1.1.7,<2.0.0',
 'minimal-activitypub>=0.4.0,<0.5.0',
 'outdated>=0.2.1,<0.3.0',
 'python-magic>=0.4.25,<0.5.0',
 'tqdm>=4.64.0,<5.0.0',
 'yt-dlp>=2023.1.6,<2024.0.0']

entry_points = \
{'console_scripts': ['tootbot = tootbot.app:start_main',
                     'tootbot_create_config = tootbot.create_config:create']}

setup_kwargs = {
    'name': 'tootbot',
    'version': '6.2.1',
    'description': 'A Python bot that looks up posts from specified subreddits and automatically posts them on Mastodon',
    'long_description': "Tootbot\n=======\n\n|Repo| |CI - Woodpecker| |Downloads|\n\n|Checked against| |Checked with| |Interrogate|\n\n|Code style| |PyPI - Python Version| |PyPI - Wheel|\n\n|GPL|\n\n\nThis is a Python bot that looks up posts from specified subreddits and automatically posts them on `Mastodon`_.\nIt is based on `reddit-twitter-bot`_.\n\nFeatures:\n---------\n\n* Tootbot posts to `Mastodon`_\n* Media from direct links, Gfycat, Imgur, Reddit, and Giphy is automatically attached in the social media post.\n  Tootbot attaches up to the first 4 pictures for imgur albums and reddit gallery posts.\n* Links that do not contain media can be skipped, ideal for meme accounts like `@babyelephantgifs`_\n* NSFW content, spoilers, and self-posts can be filtered\n* Tootbot can monitor multiple subreddits at once\n* Tootbot is fully open-source, so you don't have to give an external service full access to your social media accounts\n* Tootbot also checks the sha256 checksum of media files to stop posting of the same media file from different subreddits.\n* Tootbot can ping a `Healthchecks`_ instance for monitoring continuous operation of Tootbot\n* Optionally throttle down frequency of tooting when mastodon errors are detected.\n\n**!!! Tootbot no longer supports posting to Twitter. !!!**\n\nIf you need twitter functionality look into `reddit-twitter-bot`_ as a possible alternative.\n\n**!!! Tootbot no longer supports deleting old toots. !!!**\n\nIf you'd like to delete older toots from your Mastodon account look into `MastodonAmnesia`_ as a tool that might\nwork for you.\n\nDisclaimer\n----------\n\nThe developers of Tootbot hold no liability for what you do with this script or what happens to you by using this\nscript. Abusing this script *can* get you banned from Mastodon, so make sure to read up on proper usage of the API\nfor each site.\n\nSetup and usage\n---------------\n\nFor instructions on setting up and using Tootbot, please visit `the wiki`_\n\nSupporting Tootbot\n------------------\n\nThere are a number of ways you can support Tootbot:\n\n- Create an issue with problems or ideas you have with/for Tootboot\n- You can `buy me a coffee`_.\n- You can send me small change in Monero to the address below:\n\nMonero donation address:\n`87C65WhSDMhg4GfCBoiy861XTB6DL2MwHT3SWudhjR3LMeGEJG8zeZZ9y4Exrtx5ihavXyfSEschtH4JqHFQS2k1Hmn2Lkt`\n\nChangelog\n---------\n\nSee the `Changelog`_ for any changes introduced with each version.\n\nLicense\n-------\n\nTootbot is licences under the `GNU General Public License v3.0`_\n\n\n\n.. _Mastodon: https://joinmastodon.org/\n.. _reddit-twitter-bot: https://github.com/rhiever/reddit-twitter-bot\n.. _MastodonAmnesia: https://pypi.org/project/mastodonamnesia/\n.. _@babyelephantgifs: https://botsin.space/@babyelephantgifs\n.. _Healthchecks: https://healthchecks.io/\n.. _the wiki: https://codeberg.org/MarvinsMastodonTools/tootbot/wiki\n.. _buy me a coffee: https://www.buymeacoffee.com/marvin8\n.. _GNU General Public License v3.0: http://www.gnu.org/licenses/agpl-3.0.html\n.. _Changelog: https://codeberg.org/PyYtTools/Playlist2Podcasts/src/branch/main/CHANGELOG.rst\n\n.. |GPL| image:: https://www.gnu.org/graphics/gplv3-with-text-136x68.png\n    :alt: GPL3\n    :target: https://codeberg.org/MarvinsMastodonTools/tootbot/src/branch/main/license.txt\n\n.. |Repo| image:: https://img.shields.io/badge/repo-Codeberg.org-blue\n    :alt: Repo at Codeberg\n    :target: https://codeberg.org/MarvinsMastodonTools/tootbot\n\n.. |Downloads| image:: https://pepy.tech/badge/tootbot\n    :target: https://pepy.tech/project/tootbot\n\n.. |Code style| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :alt: Code Style: Black\n    :target: https://github.com/psf/black\n\n.. |Checked against| image:: https://img.shields.io/badge/Safety--DB-Checked-green\n    :alt: Checked against Safety DB\n    :target: https://pyup.io/safety/\n\n.. |Checked with| image:: https://img.shields.io/badge/pip--audit-Checked-green\n    :alt: Checked with pip-audit\n    :target: https://pypi.org/project/pip-audit/\n\n.. |PyPI - Python Version| image:: https://img.shields.io/pypi/pyversions/tootbot\n\n.. |PyPI - Wheel| image:: https://img.shields.io/pypi/wheel/tootbot\n\n.. |CI - Woodpecker| image:: https://ci.codeberg.org/api/badges/MarvinsMastodonTools/tootbot/status.svg\n    :target: https://ci.codeberg.org/MarvinsMastodonTools/tootbot\n\n.. |Interrogate| image:: https://codeberg.org/MarvinsMastodonTools/tootbot/raw/branch/wip2301/interrogate_badge.svg\n    :alt: Doc-string coverage\n    :target: https://interrogate.readthedocs.io/en/latest/\n",
    'author': 'marvin8',
    'author_email': 'marvin8@tuta.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://codeberg.org/MarvinsMastodonTools/tootbot',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
