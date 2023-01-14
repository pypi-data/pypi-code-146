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
 'sentence-transformers>=2.2.2,<3.0.0',
 'slug>=2.0,<3.0']

entry_points = \
{'console_scripts': ['dr-doc-search = doc_search.app:main']}

setup_kwargs = {
    'name': 'dr-doc-search',
    'version': '1.4.1',
    'description': 'Search through a document using a chat interface',
    'long_description': '# Doc Search\n\n[![PyPI](https://img.shields.io/pypi/v/dr-doc-search?style=flat-square)](https://pypi.python.org/pypi/dr-doc-search/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dr-doc-search?style=flat-square)](https://pypi.python.org/pypi/dr-doc-search/)\n[![PyPI - License](https://img.shields.io/pypi/l/dr-doc-search?style=flat-square)](https://pypi.python.org/pypi/dr-doc-search/)\n\nConverse with a book (PDF)\n\n![](assets/dr-doc-search-github-demo.gif)\n\nSee [tweet](https://twitter.com/deskriders_twt/status/1612088387984588802) for full demo.\n\n---\n\n**Documentation**: [https://namuan.github.io/dr-doc-search](https://namuan.github.io/dr-doc-search)\n\n**Source Code**: [https://github.com/namuan/dr-doc-search](https://github.com/namuan/dr-doc-search)\n\n**PyPI**: [https://pypi.org/project/dr-doc-search/](https://pypi.org/project/dr-doc-search/)\n\n---\n\n## Pre-requisites\n\n- [Tessaract OCR](https://github.com/tesseract-ocr/tesseract)\n- [ImageMagick](https://imagemagick.org/index.php)\n\n## Installation\n\n```sh\npip install dr-doc-search\n```\n\n## Example Usage\n\nThere are two steps to use this application:\n\n**1.** First, you need to create the index and generate embeddings for the PDF file.\nHere I\'m using a PDF file generated from this page [Parable of a Monetary Economy\n   ](http://heteconomist.com/parable-of-a-monetary-economy/)\n\nBefore running this, you need to set up your OpenAI API key. You can get it from [OpenAI](https://beta.openai.com/account/api-keys).\n\n```shell\nexport OPENAI_API_KEY=<your-openai-api-key>\n```\n\nThe run the following command to start the training process:\n\n```shell\ndr-doc-search --train -i ~/Downloads/parable-of-a-monetary-economy-heteconomist.pdf\n```\n\nThe training process generates some temporary files in the `OutputDir/dr-doc-search/<pdf-name>` folder under your home directory.\nHere is what it looks like:\n\n```text\n ~/OutputDir/dr-doc-search/parable-of-a-monetary-economy-heteconomist\n$ tree\n.\n├── images\n│ ├── output-1.png\n│ ├── output-10.png\n│ ├── output-11.png\n...\n│ └── output-9.png\n├── index\n│ ├── docsearch.index\n│ └── index.pkl\n├── parable-of-a-monetary-economy-heteconomist.pdf\n└── scanned\n    ├── output-1.txt\n    ...\n    └── output-9.txt\n```\n\n> **Note:**\n> It is possible to change the base of the output directory by providing the `--app-dir` argument.\n\n**2.** Now that we have the index, we can use it to start asking questions.\n\n```shell\ndr-doc-search -i ~/Downloads/parable-of-a-monetary-economy-heteconomist.pdf --input-question "How did the attempt to reduce the debut resulted in decrease in employment?"\n```\n\nOr You can open up a web interface (on port :5006) to ask questions:\n\n```shell\ndr-doc-search --web-app -i ~/Downloads/parable-of-a-monetary-economy-heteconomist.pdf\n```\n\nThere are more options for choose the start and end pages for the PDF file.\nSee the help for more details:\n\n```shell\ndr-doc-search --help\n```\n\n## Acknowledgements\n\n- [anton/@abacaj](https://twitter.com/abacaj/status/1608163940726358024) for the idea\n- [LangChain](https://github.com/hwchase17/langchain)\n- [HoloViz Panel](https://panel.holoviz.org/)\n- [OpenAI](https://beta.openai.com/)\n\n## Development\n\n* Clone this repository\n* Requirements:\n  * Python 3.7+\n  * [Poetry](https://python-poetry.org/)\n\n* Create a virtual environment and install the dependencies\n```sh\npoetry install\n```\n\n* Activate the virtual environment\n```sh\npoetry shell\n```\n\n### Validating build\n```sh\nmake build\n```\n\n### Release process\nA release is automatically published when a new version is bumped using `make bump`.\nSee `.github/workflows/build.yml` for more details.\nOnce the release is published, `.github/workflows/publish.yml` will automatically publish it to PyPI.\n\n### Disclaimer\n\nThis project is not affiliated with OpenAI.\nThe OpenAI API and GPT-3 language model are not free after the trial period.\n',
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
