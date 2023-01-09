# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cleanit', 'cleanit.data']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'babelfish>=0.6.0,<0.7.0',
 'chardet>=5.1.0,<6.0.0',
 'click>=8.1.3,<9.0.0',
 'jsonschema>=4.17.3,<5.0.0',
 'pysrt>=1.1.2,<2.0.0',
 'pyyaml>=6.0,<7.0']

entry_points = \
{'console_scripts': ['cleanit = cleanit.cli:cleanit']}

setup_kwargs = {
    'name': 'cleanit',
    'version': '0.4.6',
    'description': 'Subtitles extremely clean',
    'long_description': "# CleanIt\n\nSubtitles extremely clean.\n\n[![Latest\nVersion](https://img.shields.io/pypi/v/cleanit.svg)](https://pypi.python.org/pypi/cleanit)\n\n[![tests](https://github.com/ratoaq2/cleanit/actions/workflows/test.yml/badge.svg)](https://github.com/ratoaq2/cleanit/actions/workflows/test.yml)\n\n[![License](https://img.shields.io/github/license/ratoaq2/cleanit.svg)](https://github.com/ratoaq2/cleanit/blob/master/LICENSE)\n\n  - Project page  \n    <https://github.com/ratoaq2/cleanit>\n\n**CleanIt** is a command line tool that helps you to keep your subtitles\nclean. You can specify your own rules to detect entries to be removed or\npatterns to be replaced. Simple text matching or complex regex can be\nused. It comes with standard rules out of the box:\n\n  - ocr: Fix common OCR errors\n  - tidy: Fix common formatting issues (e.g.: extra/missing spaces after\n    punctuation)\n  - no-sdh: Remove SDH descriptions\n  - no-lyrics: Remove lyrics\n  - no-spam: Remove ads and spams\n  - no-style: Remove font style tags like \\<i\\> and \\<b\\>\n  - minimal: includes only ocr and tidy rules\n  - default: includes all rules except no-style\n\n## Usage\n\n### CLI\n\nClean subtitles:\n\n    $ cat mysubtitle.srt\n    1\n    00:00:46,464 --> 00:00:48,549\n    -And then what?\n    -| don't know.\n    \n    2\n    00:49:07,278 --> 00:49:09,363\n    - If you cross the sea\n    with an army you bought ...\n    \n    \n    $ cleanit -t default mysubtitle.en.srt\n    1 subtitle collected / 0 subtitle filtered out / 0 path ignored\n    1 subtitle saved / 0 subtitle unchanged\n    \n    $ cat mysubtitle.srt\n    1\n    00:00:46,464 --> 00:00:48,549\n    - And then what?\n    - I don't know.\n    \n    2\n    00:49:07,278 --> 00:49:09,363\n    If you cross the sea\n    with an army you bought...\n    \n    \n    $ cleanit -t ocr -t no-sdh -t tidy -l en -l pt-BR ~/subtitles/\n    423 subtitles collected / 107 subtitles filtered out / 0 path ignored\n    Cleaning subtitles  [####################################]  100%\n    268 subtitles saved / 155 subtitles unchanged\n\nUsing docker:\n\n    $ docker run -it --rm -v /medias:/medias -u $(id -u username):$(id -g username) ratoaq2/cleanit -t default /medias\n    1072 subtitles collected / 0 subtitle filtered out / 0 path ignored\n    Cleaning subtitles  [####################################]  100%\n    980 subtitle saved / 92 subtitles unchanged\n\n### API\n\n``` python\nfrom cleanit import Config, Subtitle\n\nsub = Subtitle('/subtitle/path/subtitle.en.srt')\ncfg = Config.from_path('/config/path')\nrules = cfg.select_rules(tags={'ocr'})\nif sub.clean(rules):\n    sub.save()\n```\n\n### YAML Configuration file\n\n``` yaml\ntemplates:\n  - &ocr\n    tags:\n      - ocr\n      - minimal\n      - default\n    priority: 10000\n    languages: en\n\nrules:\n  replace-l-to-I-character[ocr:en]:\n    <<: *ocr\n    patterns: '\\bl\\b'\n    replacement: 'I'\n    examples:\n      ? |\n        And if l refuse?\n      : |\n        And if I refuse?\n```\n",
    'author': 'Rato',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ratoaq2/cleanit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
