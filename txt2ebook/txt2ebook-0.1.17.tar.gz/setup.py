# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['txt2ebook',
 'txt2ebook.formats',
 'txt2ebook.formats.templates',
 'txt2ebook.formats.templates.epub',
 'txt2ebook.helpers',
 'txt2ebook.languages',
 'txt2ebook.models']

package_data = \
{'': ['*']}

install_requires = \
['CJKwrap>=2.2,<3.0',
 'EbookLib>=0.17.1,<0.18.0',
 'bs4>=0.0.1,<0.0.2',
 'cchardet>=2.1.7,<3.0.0',
 'langdetect>=1.0.9,<2.0.0',
 'regex>=2021.11.10,<2022.0.0',
 'tox-pyenv>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['tte = txt2ebook.txt2ebook:main',
                     'txt2ebook = txt2ebook.txt2ebook:main']}

setup_kwargs = {
    'name': 'txt2ebook',
    'version': '0.1.17',
    'description': 'CLI tool to convert txt file to ebook format',
    'long_description': "# txt2ebook\n\nConsole tool to convert txt file to different ebook format.\n\n## Installation\n\nStable version From PyPI:\n\n```console\npython3 -m pip install txt2ebook\n```\n\nLatest development version from GitHub:\n\n```console\npython3 -m pip install -e git+https://github.com/kianmeng/txt2ebook.git\n```\n\n## Usage\n\nShowing help message of command-line options:\n\n```console\ntxt2ebook --help\n```\n\n```console\nusage: text2ebook [-f {epub,txt}] [-t TITLE] [-l LANGUAGE] [-a AUTHOR]\n                  [-c IMAGE_FILENAME] [-w WIDTH] [-ps SEPARATOR] [-rd REGEX]\n                  [-rvc REGEX] [-rv REGEX] [-rc REGEX] [-rt REGEX] [-ra REGEX]\n                  [-rl REGEX] [-rr REGEX REGEX] [-et TEMPLATE] [-vp] [-tp] [-hn]\n                  [-fw] [-rw] [-ob] [-ow] [-v] [-d] [-h] [-V]\n                  TXT_FILENAME [EBOOK_FILENAME]\n\ntxt2ebook/tte is a cli tool to convert txt file to ebook format.\n  website: https://github.com/kianmeng/txt2ebook\n  issues: https://github.com/kianmeng/txt2ebook/issues\n\npositional arguments:\n  TXT_FILENAME          source text filename\n  EBOOK_FILENAME        converted ebook filename (default: 'TXT_FILENAME.{epub,txt}')\n\noptional arguments:\n  -f {epub,txt}         ebook format (default: '['epub', 'txt']')\n  -t TITLE              title of the ebook (default: 'None')\n  -l LANGUAGE           language of the ebook (default: 'None')\n  -a AUTHOR             author of the ebook (default: '[]')\n  -c IMAGE_FILENAME     cover of the ebook\n  -w WIDTH              width for line wrapping\n  -ps SEPARATOR         paragraph separator (default: '\\n\\n')\n  -rd REGEX             regex to delete word or phrase (default: '[]')\n  -rvc REGEX            regex to parse volume and chapter header (default: by LANGUAGE)\n  -rv REGEX             regex to parse volume header (default: by LANGUAGE)\n  -rc REGEX             regex to parse chapter header (default: by LANGUAGE)\n  -rt REGEX             regex to parse title of the book (default: by LANGUAGE)\n  -ra REGEX             regex to parse author of the book (default: by LANGUAGE)\n  -rl REGEX             regex to delete whole line (default: '[]')\n  -rr REGEX REGEX       regex to search and replace (default: '[]')\n  -et TEMPLATE          CSS template for epub ebook (default: 'clean')\n  -vp, --volume-page    generate each volume as separate page (only 'epub' format)\n  -tp, --test-parsing   test parsing for volume/chapter header\n  -hn, --header-number  convert section header from words to numbers (only zh-cn/zh-tw)\n  -fw, --fullwidth      convert ASCII character from halfwidth to fullwidth (only zh-cn/zh-tw)\n  -rw, --raise-on-warning\n                        raise exception and stop parsing if there are warnings\n  -ob, --overwrite-backup\n                        overwrite massaged and backup original TXT_FILENAME\n  -ow, --overwrite      overwrite massaged TXT_FILENAME\n  -v, --verbose         show verbosity of debugging log, use -vv, -vvv for more details\n  -d, --debug           show debugging log and stacktrace\n  -h, --help            show this help message and exit\n  -V, --version         show program's version number and exit\n```\n\nConvert a txt file into epub:\n\n```console\ntxt2book ebook.txt\n```\n\n## Copyright and License\n\nCopyright (c) 2021,2022,2023 Kian-Meng Ang\n\nThis program is free software: you can redistribute it and/or modify it under\nthe terms of the GNU Affero General Public License as published by the Free\nSoftware Foundation, either version 3 of the License, or (at your option) any\nlater version.\n\nThis program is distributed in the hope that it will be useful, but WITHOUT ANY\nWARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A\nPARTICULAR PURPOSE. See the GNU Affero General Public License for more details.\n\nYou should have received a copy of the GNU Affero General Public License along\nwith this program. If not, see <https://www.gnu.org/licenses/>.\n",
    'author': 'Kian-Meng Ang',
    'author_email': 'kianmeng@cpan.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kianmeng/txt2ebook',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
