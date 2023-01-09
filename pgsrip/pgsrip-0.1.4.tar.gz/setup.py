# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pgsrip']

package_data = \
{'': ['*']}

install_requires = \
['babelfish>=0.6.0,<0.7.0',
 'cleanit>=0.4.6,<0.5.0',
 'click>=8.1.3,<9.0.0',
 'numpy>=1.24.1,<2.0.0',
 'opencv-python>=4.7.0,<5.0.0',
 'pysrt>=1.1.2,<2.0.0',
 'pytesseract>=0.3.10,<0.4.0',
 'trakit>=0.2.1,<0.3.0']

entry_points = \
{'console_scripts': ['pgsrip = pgsrip.cli:pgsrip']}

setup_kwargs = {
    'name': 'pgsrip',
    'version': '0.1.4',
    'description': 'Rip your PGS subtitles',
    'long_description': "# PGSRip\n\nRip your PGS subtitles.\n\n[![Latest\nVersion](https://img.shields.io/pypi/v/pgsrip.svg)](https://pypi.python.org/pypi/pgsrip)\n\n[![License](https://img.shields.io/github/license/ratoaq2/pgsrip.svg)](https://github.com/ratoaq2/pgsrip/blob/master/LICENSE)\n\n  - Project page  \n    <https://github.com/ratoaq2/pgsrip>\n\n**PGSRip** is a command line tool that allows you to extract and convert\nPGS subtitles into SRT format. This tool requires MKVToolNix and\ntesseract-ocr and tessdata (<https://github.com/tesseract-ocr/tessdata>\nor <https://github.com/tesseract-ocr/tessdata_best>)\n\n## Installation\n\npgsrip:\n\n    $ pip install pgsrip\n\nMKVToolNix:\n\n    $ sudo apt-get install mkvtoolnix\n\ntesseract:\n\n    $ sudo apt-get install tesseract-ocr\n\ntessdata:\n\n    $ git clone https://github.com/tesseract-ocr/tessdata_best.git\n    export TESSDATA_PREFIX=~/tessdata_best\n\nIf you prefer to build the docker image Build Docker:\n\n    $ git clone https://github.com/ratoaq2/pgsrip.git\n    cd pgsrip\n    docker build . -t pgsrip\n\n## Usage\n\n### CLI\n\nRip from a .mkv:\n\n    $ pgsrip mymedia.mkv\n    3 PGS subtitles collected from 1 file\n    Ripping subtitles  [####################################]  100%  mymedia.mkv [5:de]\n    3 PGS subtitles ripped from 1 file\n\nRip from a .mks:\n\n    $ pgsrip mymedia.mks\n    3 PGS subtitles collected from 1 file\n    Ripping subtitles  [####################################]  100%  mymedia.mks [3:pt-BR]\n    3 PGS subtitles ripped from 1 file\n\nRip from a .sup:\n\n    $ pgsrip mymedia.en.sup\n    1 PGS subtitle collected from 1 file\n    Ripping subtitles  [####################################]  100%  mymedia.en.sup\n    1 PGS subtitle ripped from 1 file\n\nRip from a folder path:\n\n    $ pgsrip -l en -l pt-BR ~/medias/\n    11 PGS subtitles collected from 9 files / 2 files filtered out\n    Ripping subtitles  [####################################]  100%  ~/medias/mymedia.mkv [4:en]\n    11 PGS subtitles ripped from 9 files\n\nUsing docker:\n\n    $ docker run -it --rm -v /medias:/medias -u $(id -u username):$(id -g username) ratoaq2/pgsrip -l en -l de -l pt-BR -l pt /medias\n    11 PGS subtitles collected from 9 files / 2 files filtered out\n    Ripping subtitles  [####################################]  100%  /medias/mymedia.mkv [4:en]\n    11 PGS subtitles ripped from 9 files\n\n### API\n\n``` python\nfrom pgsrip import pgsrip, Mkv, Options\nfrom babelfish import Language\n\nmedia = Mkv('/subtitle/path/mymedia.mkv')\noptions = Options(languages={Language('eng')}, overwrite=True, one_per_lang=False)\npgsrip.rip(media, options)\n```\n",
    'author': 'Rato',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ratoaq2/pgsrip',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
