# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lamarkdown', 'lamarkdown.ext', 'lamarkdown.lib', 'lamarkdown.mods']

package_data = \
{'': ['*']}

install_requires = \
['cssselect>=1.1.0,<2.0.0',
 'diskcache>=5.4.0,<6.0.0',
 'lxml>=4.9.0,<5.0.0',
 'markdown>=3.3.7,<4.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'pygments>=2.12.0,<3.0.0',
 'pymdown-extensions>=9',
 'watchdog>=2.1.9,<3.0.0']

entry_points = \
{'console_scripts': ['lamd = lamarkdown.lib.lamd:main']}

setup_kwargs = {
    'name': 'lamarkdown',
    'version': '0.9',
    'description': 'A tool for compiling markdown files into standalone HTML documents, using Python Markdown. Supports Latex (given an existing Tex distribution), custom CSS and JavaScript, multiple document variations from a single source file, and a live output view.',
    'long_description': '# Lamarkdown\n\nCommand-line markdown document compiler based on Python-Markdown.\n\nThe intent is to provide a tool comparable to Latex, but with the Markdown and HTML formats in\nplace of Latex and PDF. Lamarkdown is _not_ a drop-in replacement for Latex, but it attempts to\naddress the same document-preparation use case. To this end, Lamarkdown:\n\n* Is a locally-run, command-line tool.\n* Builds a complete HTML document, where the author has complete control over the appearance\n    (though making it easy to produce something that _looks_ more like a document than a webpage).\n* Builds an entirely _self-contained_ HTML document (except where you insert external references\n    yourself), which can be stored and distributed as a standalone file.\n    * (Also currently with the exception of fonts, which are, for now, declared as links to `fonts.googleapis.com`.)\n* Allows embedding of Latex environments (or entire Latex documents), with the resulting output converted\n    to SVG format and embedded within the HTML.\n\nFurther goals of the project (sometimes also associated with Latex document preparation) are to:\n\n* Provide a live-updating feature to improve editing productivity. When enabled, the markdown file\n    is automatically re-compiled, and the HTML document auto-reloaded, when changes are detected.\n* Provide a scheme for compiling multiple variants of a single source document.\n\n\n## Requirements and Installation\n\nLamarkdown depends on Python 3.7+. To install via pip:\n\n`$ pip install lamarkdown`\n\nThis will resolve dependencies on other PyPi packages (including "markdown", others).\n\nHowever, to embed Latex code, you need to a Latex distribution (e.g., Texlive), which must be \ninstalled separately. The actual commands are configurable. By default, Lamarkdown\'s Latex \nextension runs \'xelatex\' and \'dvisvgm\'.\n\n\n## Basic usage\n\nTo compile `mydocument.md` into `mydocument.html`, just run:\n\n`$ lamd mydocument.md`\n\n(Or `lamd.py` if appropriate.)\n\nYou can enable the live-update mode using `-l`/`--live`:\n\n`$ lamd -l mydoc.md`\n\nThis will launch a local web-server and a web-browser, and will keep `mydoc.html` in sync with any\nchanges made to `mydoc.md`, until you press Ctrl+C in the terminal.\n\n\n## Wiki\n\nFor detailed documentation, see [the wiki](https://bitbucket.org/cooperdja/lamarkdown/wiki/).\n',
    'author': 'David J A Cooper',
    'author_email': 'dave@djac.au',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://bitbucket.org/cooperdja/lamarkdown',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
