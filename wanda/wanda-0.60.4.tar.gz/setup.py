# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wanda']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.1.0,<10.0.0',
 'appdirs>=1.4.4,<2.0.0',
 'cloudscraper>=1.2.60,<2.0.0',
 'colorthief>=0.2.1,<0.3.0',
 'filetype>=1.0.13,<2.0.0',
 'lxml>=4.9.0,<5.0.0',
 'musicbrainzngs>=0.7.1,<0.8.0',
 'screeninfo>=0.8,<0.9']

entry_points = \
{'console_scripts': ['wanda = wanda.wanda:run']}

setup_kwargs = {
    'name': 'wanda',
    'version': '0.60.4',
    'description': 'Set wallpapers with keywords or randomly',
    'long_description': '# wanda\nScript to set wallpaper using keyword or randomly\n\n[![Codacy Badge](https://app.codacy.com/project/badge/Grade/7c33b1c42b8d4a3fb80c74c9c8ececb9)](https://www.codacy.com/gl/kshib/wanda/dashboard?utm_source=gitlab.com&amp;utm_medium=referral&amp;utm_content=kshib/wanda&amp;utm_campaign=Badge_Grade)\n[![PyPI](https://img.shields.io/pypi/v/wanda)](https://pypi.org/project/wanda/)\n[![PyPI - Downloads](https://img.shields.io/pypi/dm/wanda)](https://pypistats.org/packages/wanda)\n[![PyPI - License](https://img.shields.io/pypi/l/wanda)](https://tldrlegal.com/license/mit-license)\n[![codecov](https://codecov.io/gl/kshib/wanda/branch/main/graph/badge.svg?token=L88CXOYRTW)](https://codecov.io/gl/kshib/wanda)\n[![Gitlab pipeline](https://img.shields.io/gitlab/pipeline-status/kshib/wanda?branch=main)](https://gitlab.com/kshib/wanda/-/pipelines)\n\n## Installation / Update\n```\npip install wanda -U\n```\n\nFor termux, you will need the following packages:\n```\npip install --upgrade pip\npkg in libxml2 libxslt libjpeg-turbo\n```\n\nFor issues installing pillow refer this [document](https://pillow.readthedocs.io/en/stable/installation.html)\n\n\n## Usage\n```\nwanda\nwanda -t mountain\nwanda -s earthview\nwanda -s wallhaven -t japan\n```\n`wanda -h` for more details\n\n## Notes\n- By default, the source is [unsplash](https://unsplash.com).\n- Some sources may have inapt images. Use them at your own risk.\n\n## Supported sources\n\n- [4chan](https://boards.4chan.org) via [Rozen Arcana](https://archive.alice.al)\n- [500px](https://500px.com)\n- [artstation](https://artstation.com)\n- [imgur](https://imgur.com) via [rimgo](https://rimgo.pussthecat.org)\n- [earthview](https://earthview.withgoogle.com)\n- local\n- [picsum](https://picsum.photos)\n- [reddit](https://reddit.com)\n- [unsplash](https://unsplash.com)\n- [wallhaven](https://wallhaven.cc)\n\n## Automate (For linux)\n* To set wallpaper at regular intervals automatically:\n\n0. (For termux) Install:\n```\ntermux-wake-lock\npkg in cronie termux-services nano\nsv-enable crond\n```\n1. Edit crontab\n```\ncrontab -e\n```\n2. Set your desired interval. For hourly:\n```\n@hourly wanda -t mountains\n```\n[(more examples)](https://crontab.guru/examples.html)\n\n4. ctrl+o to save, ctrl+x to exit the editor\n\n## Build\n[python](https://www.python.org/downloads/) and [poetry](https://python-poetry.org/) are needed\n```\ngit clone https://gitlab.com/kshib/wanda.git && cd wanda\npoetry install\npoetry build\n```\n\n## Uninstall\n```\npip uninstall wanda\n```\n\n## Shell\nOlder versions can be found [here (android)](https://gitlab.com/kshib/wanda/-/tree/sh-android) and [here (desktop)](https://gitlab.com/kshib/wanda/-/tree/sh-desktop)\n\n## Issues\nThe script is tested on Manjaro+KDE and Android+Termux and Windows 11.\n\nOn Windows, you might need to set wallpaper mode to slideshow with folder as `C:\\Users\\%username%\\wanda`\n\n## License\nMIT\n',
    'author': 'kshib',
    'author_email': 'ksyko@pm.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/kshib/wanda',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
