# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['better_highlighting',
 'better_highlighting.components',
 'better_highlighting.components.lexers_and_styles']

package_data = \
{'': ['*']}

install_requires = \
['Pygments>=2.11.2,<3.0.0',
 'pandas>=1.4.1,<2.0.0',
 'pytest>=7.2.0,<8.0.0',
 'tabulate>=0.8.9,<0.9.0']

setup_kwargs = {
    'name': 'better-highlighting',
    'version': '2.0.0',
    'description': 'Small tool for text and syntax highlight.',
    'long_description': '[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)\n\n# Better highlighting\n\n\n### Usage:\nThis tool is designed for beautiful text formatting in the terminal. It is highly specialized, prints in terminal highlighted text \nin more readable form. \nIt also can render \'pretty\' table and python\'s iterators syntax.\n\n### Example:\n<img src="https://user-images.githubusercontent.com/21011049/160372378-32acc15e-1cfa-4987-bce7-6dfd34ec3ab2.png"></img> \n\n### Text styles\n<table>\n<th>Styles</th>\n<tr><td>ansiblack</td></tr>\n<tr><td>bold</td></tr>\n<tr><td>italic</td></tr>\n<tr><td>underline</td></tr>\n</table>\n\n\n### Colors\nColors specified using ansi* are converted to a default set of RGB colors when used with formatters other than the terminal-256 formatter.\n\nBy definition of ANSI, the following colors are considered “light” colors, and will be rendered by most terminals as bold:\n\n* “brightblack” (darkgrey), “brightred”, “brightgreen”, “brightyellow”, “brightblue”, “brightmagenta”, “brightcyan”, “white”\n\nThe following are considered “dark” colors and will be rendered as non-bold:\n\n* “black”, “red”, “green”, “yellow”, “blue”, “magenta”, “cyan”, “gray”\n\n<table>\n<th>Color names</th>\n<tr><td>ansiblack</td></tr>\n<tr><td>ansired</td></tr>\n<tr><td>ansigreen</td></tr>\n<tr><td>ansiyellow</td></tr>\n<tr><td>ansiblue</td></tr>\n<tr><td>ansimagenta</td></tr>\n<tr><td>ansibrightblack</td></tr>\n<tr><td>ansibrightred</td></tr>\n<tr><td>ansibrightgreen</td></tr>\n<tr><td>ansibrightyellow</td></tr>\n<tr><td>ansibrightblue</td></tr>\n<tr><td>ansibrightmagenta</td></tr>\n<tr><td>ansibrightcyan</td></tr>\n<tr><td>ansiwhite</td></tr>\n</table>\n',
    'author': 'vskarinov',
    'author_email': 'skarinov27@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vskarinov/better_highlighting',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
