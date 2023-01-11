# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['subtitle_parser']
install_requires = \
['chardet>=4,<6']

setup_kwargs = {
    'name': 'subtitle-parser',
    'version': '1.2.0',
    'description': 'Parser for SRT and WebVTT subtitle files',
    'long_description': "subtitle-parser\n===============\n\nThis is a simple Python library for parsing subtitle files in SRT or WebVTT format.\n\nHow to use stand-alone?\n-----------------------\n\nYou can use this as a script to convert subtitles to HTML or CSV.\n\nIf you have installed it using `pip install subtitle-parser`, use `python3 -m subtitle_parser`. If you have cloned this repository or downloaded the file, use `python3 subtitle_parser.py`.\n\nExamples:\n\n```\n$ python3 subtitle_parser.py --to csv Zoom_transcript.vtt --output transcript.csv\n```\n\n```\n$ python3 -m subtitle_parser --to html episode.srt --input-charset iso-8859-15 --output dialogue.html\n```\n\nHow to use as a library?\n------------------------\n\n```python\nimport subtitle_parser\n\nwith open('some_file.srt', 'r') as input_file:\n    parser = subtitle_parser.SrtParser(input_file)\n    parser.parse()\n\nparser.print_warnings()\n\nfor subtitle in parser.subtitles:\n    print(subtitle.text)\n```\n",
    'author': 'Remi Rampin',
    'author_email': 'remi@rampin.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/remram44/subtitle-parser',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
