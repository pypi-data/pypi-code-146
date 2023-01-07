# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['doc_search', 'doc_search.workflow']

package_data = \
{'': ['*']}

install_requires = \
['faiss-cpu>=1.7.3,<2.0.0',
 'langchain>=0.0.57,<0.0.58',
 'openai>=0.25.0,<0.26.0',
 'panel>=0.14.2,<0.15.0',
 'py-executable-checklist==1.3.1',
 'pypdf>=3.2.0,<4.0.0',
 'pytest>=7.2.0,<8.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'rich>=13.0.0,<14.0.0',
 'slug>=2.0,<3.0']

entry_points = \
{'console_scripts': ['dr-doc-search = doc_search.app:main']}

setup_kwargs = {
    'name': 'dr-doc-search',
    'version': '1.2.0',
    'description': 'Search through a document using a chat interface',
    'long_description': '# Doc Search\n\n[![PyPI](https://img.shields.io/pypi/v/dr-doc-search?style=flat-square)](https://pypi.python.org/pypi/dr-doc-search/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dr-doc-search?style=flat-square)](https://pypi.python.org/pypi/dr-doc-search/)\n[![PyPI - License](https://img.shields.io/pypi/l/dr-doc-search?style=flat-square)](https://pypi.python.org/pypi/dr-doc-search/)\n\n\n---\n\n**Documentation**: [https://namuan.github.io/dr-doc-search](https://namuan.github.io/dr-doc-search)\n\n**Source Code**: [https://github.com/namuan/dr-doc-search](https://github.com/namuan/dr-doc-search)\n\n**PyPI**: [https://pypi.org/project/dr-doc-search/](https://pypi.org/project/dr-doc-search/)\n\n---\n\nConverse with an ebook (PDF)\n\n## Pre-requisites\n\n- [Tessaract OCR](https://github.com/tesseract-ocr/tesseract)\n- [ImageMagick](https://imagemagick.org/index.php)\n\n## Installation\n\n```sh\npip install dr-doc-search\n```\n\n## Example Usage\n\n```shell\ndr-doc-search --help\n```\n\n## Development\n\n* Clone this repository\n* Requirements:\n  * Python 3.7+\n  * [Poetry](https://python-poetry.org/)\n\n* Create a virtual environment and install the dependencies\n```sh\npoetry install\n```\n\n* Activate the virtual environment\n```sh\npoetry shell\n```\n\n### Validating build\n```sh\nmake build\n```\n\n### Release process\nA release is automatically published when a new version is bumped using `make bump`.\nSee `.github/workflows/build.yml` for more details.\nOnce the release is published, `.github/workflows/publish.yml` will automatically publish it to PyPI.\n',
    'author': 'namuan',
    'author_email': 'github@deskriders.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://namuan.github.io/dr-doc-search',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9.0,<4.0',
}


setup(**setup_kwargs)
