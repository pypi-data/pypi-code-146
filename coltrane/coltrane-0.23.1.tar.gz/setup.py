# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['coltrane',
 'coltrane.config',
 'coltrane.management',
 'coltrane.management.commands',
 'coltrane.templatetags']

package_data = \
{'': ['*'], 'coltrane': ['templates/coltrane/*']}

install_requires = \
['Django>3.0',
 'click>=8.0.0,<9.0.0',
 'dateparser>=1.1.0,<2.0.0',
 'django-browser-reload>=1.3.0,<2.0.0',
 'django-fastdev>=1.3.0,<2.0.0',
 'halo>=0.0.31,<0.0.32',
 'markdown2>=2.4.2,<3.0.0',
 'python-dotenv>0.17',
 'rich-click>=0.2.0,<0.3.0']

extras_require = \
{'deploy': ['gunicorn>=20.1.0,<21.0.0', 'whitenoise>=5.3.0,<6.0.0'],
 'docs': ['Sphinx>=4.3.2,<5.0.0',
          'linkify-it-py>=1.0.3,<2.0.0',
          'myst-parser>=0.16.1,<0.17.0',
          'furo>=2021.11.23,<2022.0.0',
          'sphinx-copybutton>=0.4.0,<0.5.0',
          'sphinx-autobuild>=2021.3.14,<2022.0.0',
          'toml',
          'attrs>=21.4.0,<22.0.0'],
 'mistune': ['mistune>=3.0.0rc4,<4.0.0',
             'python-frontmatter>=1.0.0,<2.0.0',
             'pygments>=2.7.3',
             'minestrone>=0.6.2']}

entry_points = \
{'console_scripts': ['coltrane = coltrane.console:cli']}

setup_kwargs = {
    'name': 'coltrane',
    'version': '0.23.1',
    'description': 'A simple content site framework that harnesses the power of Django without the hassle.',
    'long_description': '<p align="center">\n  <a href="https://coltrane.readthedocs.io"><h1 align="center">coltrane</h1></a>\n</p>\n<p align="center">A simple content site framework that harnesses the power of Django without the hassle 🎵</p>\n\n![PyPI](https://img.shields.io/pypi/v/coltrane?color=blue&style=flat-square)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/coltrane?color=blue&style=flat-square)\n![GitHub Sponsors](https://img.shields.io/github/sponsors/adamghill?color=blue&style=flat-square)\n<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->\n![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square)\n<!-- ALL-CONTRIBUTORS-BADGE:END -->\n\n📖 Complete documentation: https://coltrane.readthedocs.io\n\n📦 Package located at https://pypi.org/project/coltrane/\n\n## ⭐ Features\n\n- Can either generate a static HTML site, be deployed as a standalone Django site, or integrated into an existing Django site\n- Reads markdown content and renders it in HTML\n- Can use data from JSON files in templates and markdown content\n- Automatic generation of `sitemap.xml` and `rss.xml` files\n- Can also serve non-markdown files like `robots.txt`\n- [Live re-rendering of markdown and data](https://twitter.com/adamghill/status/1487522925393715205) when markdown or JSON data files are saved with the magic of https://github.com/adamchainz/django-browser-reload\n- All the power of Django templates, template tags, and filters inside markdown files\n- Can include other Django apps for additional functionality\n- Custom Template tags are supported and are enabled automatically for use in markdown content\n- Opinionated standalone Django project setup where deployment (including static files) just works "out of the box"\n\n## ⚡ Quick start for a new static site\n\n1. `mkdir new-site && cd new-site` to create a new folder\n1. `poetry init --no-interaction --dependency \'coltrane:<1\' && poetry install` to create a new virtual environment and install the `coltrane` package\n1. `poetry run coltrane create` to create the folder structure for a new site\n1. Update `content/index.md`\n1. `poetry run coltrane play` for a local development server\n1. Go to http://localhost:8000 to see the updated markdown rendered into HTML\n1. `poetry run coltrane record` to output the rendered HTML files\n\n### Optional installation\n\n- Enable `watchman` for less resource-intensive autoreload on MacOS: `brew install watchman`\n\n## ➕ How to add new content\n\nAdd markdown files or sub-directories with markdown files to the `content` directory and they will automatically have routes created that can be requested.\n\n**Example markdown files**\n\n```\ncontent/index.md\ncontent/about.md\ncontent/articles/this-is-the-first-article.md\n```\n\n**`poetry run coltrane play` will serve these URLs**\n\n- `http://localhost:8000/` which serves HTML generated from the `/content/index.md` file\n- `http://localhost:8000/about/` which serves HTML generated from the `/content/about.md` file\n- `http://localhost:8000/articles/this-is-the-first-article/` which serves HTML generated from the `/content/articles/this-is-the-first-article.md` file\n- `http://localhost:8000/not-there/` will 404\n\n**`poetry run coltrane record` will create these HTML files for a static site**\n\n- `output/index.html`\n- `output/about/index.html`\n- `output/articles/this-is-the-first-article/index.html`\n\nRead all of the documentation at https://coltrane.readthedocs.io.\n\n## Contributors ✨\n\nThanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):\n\n<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->\n<!-- prettier-ignore-start -->\n<!-- markdownlint-disable -->\n<table>\n  <tbody>\n    <tr>\n      <td align="center"><a href="https://github.com/Tobi-De"><img src="https://avatars.githubusercontent.com/u/40334729?v=4?s=100" width="100px;" alt="Tobi DEGNON"/><br /><sub><b>Tobi DEGNON</b></sub></a><br /><a href="https://github.com/adamghill/coltrane/commits?author=Tobi-De" title="Tests">⚠️</a> <a href="https://github.com/adamghill/coltrane/commits?author=Tobi-De" title="Code">💻</a></td>\n    </tr>\n  </tbody>\n  <tfoot>\n    \n  </tfoot>\n</table>\n\n<!-- markdownlint-restore -->\n<!-- prettier-ignore-end -->\n\n<!-- ALL-CONTRIBUTORS-LIST:END -->\n\nThis project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!\n',
    'author': 'adamghill',
    'author_email': 'adam@adamghill.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/adamghill/coltrane/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
