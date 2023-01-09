# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yark']

package_data = \
{'': ['*'], 'yark': ['templates/*']}

install_requires = \
['Flask>=2.2.2,<3.0.0',
 'colorama>=0.4.6,<0.5.0',
 'requests>=2.28.1,<3.0.0',
 'yt-dlp>=2023.1.2,<2024.0.0']

entry_points = \
{'console_scripts': ['yark = yark.cli:_cli']}

setup_kwargs = {
    'name': 'yark',
    'version': '1.2.3',
    'description': 'YouTube archiving made simple.',
    'long_description': '<!-- TODO: logo; #2 <https://github.com/Owez/yark/issues/2> -->\n<!-- TODO: add when logos done; #2 <https://github.com/Owez/yark/issues/2>: <h1 align="center">yark</h1> -->\n\n# Yark\n\nYouTube archiving made simple.\n\n[Installation](#installation) · [Managing your Archive](#managing-your-archive) · [Viewing your Archive](#viewing-your-archive)\n\nYark lets you continuously archive all videos and metadata for YouTube channels. You can also view your archive as a seamless offline website ✨\n\n## Installation\n\nTo install Yark, simply download [Python 3.9+](https://www.python.org/downloads/) and [FFmpeg](https://ffmpeg.org/) (optional), then run the following:\n\n```shell\n$ pip3 install yark\n```\n\n## Managing your Archive\n\nOnce you\'ve installed Yark, think of a name for your archive (e.g., "foobar") and copy the target\'s url:\n\n```shell\n$ yark new foobar https://www.youtube.com/channel/UCSMdm6bUYIBN0KfS2CVuEPA\n```\n\nNow that you\'ve created the archive, you can tell Yark to download all videos and metadata using the refresh command:\n\n```shell\n$ yark refresh foobar\n```\n\nOnce everything has been downloaded, Yark will automatically give you a status report of what\'s changed since the last refresh:\n\n<p><img src="examples/image/../images/cli_dark.png" alt="Report Demo" title="Report Demo" width="600" /></p>\n\n## Viewing your Archive\n\nViewing you archive is easy, just type `view` with your archives name:\n\n```shell\n$ yark view foobar\n```\n\nThis will pop up an offline website in your browser letting you watch all videos 🚀\n\n<p><img src="https://raw.githubusercontent.com/Owez/yark/master/examples/images/viewer_light.png" alt="Viewer Demo" title="Viewer Demo" width=650 /></p>\n\nUnder each video is a rich history report filled with timelines and graphs, as well as a noting feature which lets you add timestamped and permalinked comments 👐\n\n<p><img src="https://raw.githubusercontent.com/Owez/yark/master/examples/images/viewer_stats_light.png" alt="Viewer Demo – Stats" title="Viewer Demo – Stats" width=650 /></p>\n\nLight and dark modes are both available and automatically apply based on the system\'s theme.\n\n## Details\n\nHere are some things to keep in mind when using Yark; the good and the bad:\n\n- Don\'t create a new archive again if you just want to update it, Yark accumulates all new metadata for you via timestamps\n- Feel free to suggest new features via the issues tab on this repository\n- Scheduling isn\'t a feature just yet, please use [`cron`](https://en.wikipedia.org/wiki/Cron) or something similar!\n\n## Archive Format\n\nThe archive format itself is simple and consists of a directory-based structure with a core metadata file and all thumbnail/video data in their own directories as typical files:\n\n- `[name]/` – Your self-contained archive\n  - `yark.json` –\xa0Archive file with all metadata\n  - `yark.bak` – Backup archive file to protect against data damage\n  - `videos/` – Directory containing all known videos\n    - `[id].*` – Files containing video data for YouTube videos\n  - `thumbnails/` – Directory containing all known thumbnails\n    - `[hash].png` – Files containing thumbnails with its BLAKE2 hash\n\nIt\'s best to take a few minutes to familiarize yourself with your archive by looking at files which look interesting to you in it, everything is quite readable.\n',
    'author': 'Owen Griffiths',
    'author_email': 'root@ogriffiths.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/owez/yark',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
