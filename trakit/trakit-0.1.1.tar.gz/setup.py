# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['trakit', 'trakit.converters']

package_data = \
{'': ['*'], 'trakit': ['data/*']}

install_requires = \
['babelfish>=0.6.0,<0.7.0', 'rebulk>=3.1.0,<4.0.0']

entry_points = \
{'console_scripts': ['trakit = trakit.__main__:main']}

setup_kwargs = {
    'name': 'trakit',
    'version': '0.1.1',
    'description': 'Guess additional information from track titles',
    'long_description': '# TrakIt\nGuess additional information from track titles\n\n[![Latest\nVersion](https://img.shields.io/pypi/v/trakit.svg)](https://pypi.python.org/pypi/trakit)\n\n[![tests](https://github.com/ratoaq2/trakit/actions/workflows/test.yml/badge.svg)](https://github.com/ratoaq2/trakit/actions/workflows/test.yml)\n\n[![License](https://img.shields.io/github/license/ratoaq2/trakit.svg)](https://github.com/ratoaq2/trakit/blob/master/LICENSE)\n\n  - Project page  \n    <https://github.com/ratoaq2/trakit>\n\n## Info\n\n**TrakIt** is a track name parser.\nIt is a tiny library created to solve a very specific problem.\nIt\'s very common that video files do not have precise metadata information, \nwhere you can have multiple subtitle tracks tagged as **Portuguese**, \nbut one of them is actually **Brazilian Portuguese**:\n```json lines\n{\n  "codec": "SubRip/SRT",\n  "id": 19,\n  "properties": {\n    "codec_id": "S_TEXT/UTF8",\n    "codec_private_length": 0,\n    "default_track": false,\n    "enabled_track": true,\n    "encoding": "UTF-8",\n    "forced_track": false,\n    "language": "por",\n    "language_ietf": "pt",\n    "number": 20,\n    "text_subtitles": true,\n    "track_name": "Português",\n    "uid": 160224385584803173\n  }\n}\n\n{\n  "codec": "SubRip/SRT",\n  "id": 20,\n  "properties": {\n    "codec_id": "S_TEXT/UTF8",\n    "codec_private_length": 0,\n    "default_track": false,\n    "enabled_track": true,\n    "encoding": "UTF-8",\n    "forced_track": false,\n    "language": "por",\n    "language_ietf": "pt",\n    "number": 21,\n    "text_subtitles": true,\n    "track_name": "Português (Brasil)",\n    "uid": 1435945803220205\n  }\n}\n```\nOr you have multiple audio tracks in **English**,\nbut one of them is **British English** (`British English Forced (PGS)`) and others are **American English**\n(`American English (PGS)`)\n\nGiven a track name, **TrakIt** can guess the language:\n\n```bash\n> trakit "Português (Brasil)"\n{\n  "language": "pt-BR"\n}\n```\n\n**TrakIt** is also able to identify:\n* SDH: Subtitles for the Deaf or Hard of Hearing\n* Forced flag\n* Closed captions\n* Alternate version tracks\n* Commentary tracks\n\n```bash\n>> trakit "British English (SDH) (PGS)"\n{\n  "language": "en-GB",\n  "hearing_impaired": true\n}\n\n>> trakit "English CC (SRT)"\n{\n  "language": "en",\n  "closed_caption": true\n}\n\n>> trakit "Cast and Crew Commentary (English AC3 Stereo)"\n{\n  "language": "en",\n  "commentary": true\n}\n\n>> trakit "Français Forced (SRT)"\n{\n  "language": "fr",\n  "forced": true\n}\n```\n\n**TrakIt** is not a release parser. Use [GuessIt](https://github.com/guessit-io/guessit)\n\n**TrakIt** is not a video metadata extractor.\nUse [KnowIt](https://github.com/ratoaq2/knowit).\nKnowIt already uses **trakit** to enhance the extracted information\n\n## Installation\n\n**TrakIt** can be installed as a regular python module by running:\n\n    $ [sudo] pip install trakit\n\nFor a better isolation with your system you should use a dedicated\nvirtualenv or install for your user only using the `--user` flag.\n\n## Data\n* Available languages are the same supported by [Diaoul/babelfish](https://github.com/Diaoul/babelfish)\n* Localized country names were fetched from [mledoze/countries](https://github.com/mledoze/countries)\n* Localized language names were fetched from [mozilla/language-mapping-list](https://github.com/mozilla/language-mapping-list)\n',
    'author': 'Rato',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ratoaq2/trakit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
