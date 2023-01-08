# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lyrics_translator', 'lyrics_translator.core']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'lyricsgenius>=3.0.1,<4.0.0',
 'python-docx>=0.8.11,<0.9.0',
 'python-dotenv>=0.20.0,<0.21.0',
 'sacremoses>=0.0.53,<0.0.54',
 'sentencepiece>=0.1.96,<0.2.0',
 'tqdm>=4.64.1,<5.0.0',
 'transformers[torch]>=4.20.1,<5.0.0']

entry_points = \
{'console_scripts': ['lyrics-translator = lyrics_translator.console:main']}

setup_kwargs = {
    'name': 'lyrics-translator',
    'version': '0.3.0',
    'description': '🎵 LyricsTranslator - automated lyrics translation',
    'long_description': '\n<!-- <p align="center">\n<img src="https://github.com/MauroLuzzatto/lyrics-translator/blob/main/docs/img/logo.jpg" width="200" height="200"/>\n</p> -->\n\n<h1 align="center">🎵 LyricsTranslator - automated lyrics translation</h1>\n\n\n\n<p align="center">\n\n<a href="https://pypi.python.org/pypi/lyrics-translator" target="_blank">\n    <img src="https://img.shields.io/pypi/v/lyrics-translator.svg" alt="pypi version">\n</a>\n\n<a href="https://pypi.org/project/lyrics-translator" target="_blank">\n    <img src="https://img.shields.io/pypi/pyversions/lyrics-translator.svg" alt="Supported versions">\n</a>\n\n<a href="https://github.com/ambv/black" target="_blank">\n    <img src="https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square" alt="Code style: black">\n\n<a href="https://pycqa.github.io/isort/" target="_blank">\n    <img src="https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336" alt="Imports: isort">\n\n\n</p>\n\n---\n\n**Documentation**: <a href="https://mauroluzzatto.github.io/lyrics-translator" target="_blank">https://mauroluzzatto.github.io/lyrics-translator</a>\n\n**Source Code**: <a href="https://github.com/MauroLuzzatto/lyrics-translator" target="_blank">https://github.com/MauroLuzzatto/lyrics-translator</a>\n\n---\n\n\nThe `LyricsTranslator` downloads lyrics from [genius](https://genius.com/) and uses 🤗[hugging face](https://huggingface.co/) to translate the lyrics into a target language.\n\n\nAll languages that are supported by [OPUS-MT](https://github.com/Helsinki-NLP/Opus-MT) are available for translation.The full list of list of languages can be found on 🤗[hugging face](https://huggingface.co/models?other=marian).\n\n- German: `de`\n- Swedish: `sv`\n- French: `fr`\n- Spanish: `es` \n- Chinese: `zh`\n- Japanese: `ja`\n- Portuguese: `pt`\n- Arabic: `ar`\n- Italian: `it`\n\nand many more ...\n\n\n\n\n\n## Install\n\n```\npip install lyrics-translator\n```\n\n## Setup\nTo use the `LyricsTranslator` you will have to [get an API token](https://docs.genius.com/#/getting-started-h1) from `genius` add the API token to the `.env` file:\n\n```txt\nGENIUS_ACCESS_TOKEN=<replace-me-with-your-genius-api-token>\n```\n\n## Supported Languages\n\n\n\n## Usage\n<!--\n📚 A comprehensive example of the `explainy` API can be found in this ![Jupyter Notebook](https://github.com/MauroLuzzatto/explainy/blob/main/examples/01-explainy-intro.ipynb)\n\n📖 Or in the [example section](https://explainy.readthedocs.io/en/latest/examples/01-explainy-intro.html) of the documentation -->\n\n\n```python\nfrom lyrics_translator import LyricsTranslator\n\nsong = "Surfin\' U.S.A."\nartist = "The Beach Boys"\nlanguage = "de"\n\ntranslator = LyricsTranslator(language)\nlyrics = translator.get_song_translation(song, artist)\nprint(lyrics)\n```\nOutput:\n```\nSurfin’ USA Lyrics[Verse 1]\nWenn jeder einen Ozean hätte\nÜberall in den USA\nDann würde jeder surfen\nWie Californi-a\nSie würden ihre Taschen tragen.\nAuch Huarache Sandalen\nEin stumpfes stumpfes blond Haar\nSurfin\' U.S.A\n\n[Korus]\nSie würden sie surfen in Del Mar\n(Innen, Außen, USA)\nVentura County Line\n(Innen, Außen, USA)\nSanta Cruz und Trestles\n(Innen, Außen, USA)\nAustraliens Narrabeen\n(Innen, Außen, USA)\nÜberall in Manhattan\n(Innen, Außen, USA)\nUnd den Doheny Way hinunter\n(Innen, Außen)\n[Anschlag]\nJeder ist surfin\'\nSurfin\' U.S.A\n\n[Zwischenruf 2]\nWir werden alle diese Route planen.\nWir werden wirklich bald\nWir wischen unsere Surfbretter ab\nWir können auf Juni nicht warten\nWir werden alle für den Sommer weg sein\nWir sind auf surfari zu bleiben\nSagen Sie dem Lehrer, wir surfen\nSurfin\' U.S.A\n\n[Korus]\nHaggerties und Swamis\n(Innen, Außen, USA)\nPalisaden im Pazifik\n(Innen, Außen, USA)\nSan Onofre und der Sonnenuntergang\n(Innen, Außen, USA)\nRedondo Beach LA\n(Innen, Außen, USA)\nGanz La Jolla\n(Innen, Außen, USA)\nIn der Bucht von Wa\'imea\n(Innen, Außen)\n[Anschlag]\nJeder ist surfin\'\nSurfin\' U.S.A\n\n[Instrumental Interlude]\n\n[Outro]\nJeder ist surfin\'\nSurfin\' U.S.A\n\nJeder ist surfin\'\nSurfin\' U.S.A\n\nJeder ist surfin\'\nSurfin\' U.S.A\n\nJeder ist surfin\'\nSurfin\' U.S.A\n```\n',
    'author': 'Mauro Luzzatto',
    'author_email': 'mauroluzzatto@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://mauroluzzatto.github.io/lyrics-translator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
