# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['playlist2podcast']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.0.0,<10.0.0',
 'arrow>=1.2.1,<2.0.0',
 'feedgen>=0.9.0,<0.10.0',
 'outdated>=0.2.1,<0.3.0',
 'requests>=2.28.1,<3.0.0',
 'rich>=13.0.0,<14.0.0',
 'typing-extensions>=4.2.0,<5.0.0',
 'yt-dlp>=2023.1.2,<2024.0.0']

entry_points = \
{'console_scripts': ['playlist2podcast = '
                     'playlist2podcast.playlist_2_podcast:main']}

setup_kwargs = {
    'name': 'playlist2podcast',
    'version': '0.6.2',
    'description': 'Creates podcast feed from playlist URL',
    'long_description': 'Playlist2Podcast\n================\n\n|Repo| |Downloads| |Code style| |Checked against| |Checked with| |PyPI - Python Version| |PyPI - Wheel|\n|CI - Woodpecker| |AGPL|\n\n\nPlaylist2Podcast is a command line tool that takes a Youtube playlist, downloads the audio portion of the videos on that\nlist, and creates a podcast feed from this.\n\nPlaylist2Podcast:\n\n1) downloads and converts the videos in one or more playlists to opus audio only files,\n2) downloads thumbnails and converts them to JPEG format, and\n3) creates a podcast feed with the downloaded videos and thumbnails.\n\nEasiest way to use Playlist2Podcast is to use `pipx` to install it from PyPi. Then you can simply use\n`playlist2podcast` on the command line run it.\n\nPlaylist2Podcast will ask for all necessary parameters when run for the first time and store them in `config.json`\nfile in the current directory.\n\nSee the `Changelog`_ for any changes introduced with each version.\n\nPlaylist2Podcast is licences under the `GNU Affero General Public License v3.0`_\n\n.. _GNU Affero General Public License v3.0: http://www.gnu.org/licenses/agpl-3.0.html\n\n.. |AGPL| image:: https://www.gnu.org/graphics/agplv3-with-text-162x68.png\n    :alt: AGLP 3 or later\n    :target: https://codeberg.org/PyYtTools/Playlist2Podcasts/src/branch/main/LICENSE.md\n\n.. |Repo| image:: https://img.shields.io/badge/repo-Codeberg.org-blue\n    :alt: Repo at Codeberg\n    :target: https://codeberg.org/PyYtTools/Playlist2Podcasts\n\n.. |Downloads| image:: https://pepy.tech/badge/playlist2podcast\n    :target: https://pepy.tech/project/playlist2podcast\n\n.. |Code style| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :alt: Code Style: Black\n    :target: https://github.com/psf/black\n\n.. |Checked against| image:: https://img.shields.io/badge/Safety--DB-Checked-green\n    :alt: Checked against Safety DB\n    :target: https://pyup.io/safety/\n\n.. |Checked with| image:: https://img.shields.io/badge/pip--audit-Checked-green\n    :alt: Checked with pip-audit\n    :target: https://pypi.org/project/pip-audit/\n\n.. |PyPI - Python Version| image:: https://img.shields.io/pypi/pyversions/playlist2podcast\n\n.. |PyPI - Wheel| image:: https://img.shields.io/pypi/wheel/playlist2podcast\n\n.. |CI - Woodpecker| image:: https://ci.codeberg.org/api/badges/PyYtTools/Playlist2Podcasts/status.svg\n    :target: https://ci.codeberg.org/PyYtTools/Playlist2Podcasts\n\n.. _Changelog: https://codeberg.org/PyYtTools/Playlist2Podcasts/src/branch/main/CHANGELOG.rst\n',
    'author': 'marvin8',
    'author_email': 'marvin8@tuta.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://codeberg.org/PyYtTools/Playlist2Podcasts',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.4,<4.0.0',
}


setup(**setup_kwargs)
