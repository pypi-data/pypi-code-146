# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['doc_extractor']

package_data = \
{'': ['*']}

install_requires = \
['docx2txt>=0.8,<0.9',
 'html2text>=2020.1.16,<2021.0.0',
 'pdfplumber>=0.7.6,<0.8.0',
 'pymupdf>=1.21.1,<2.0.0',
 'pypdf2>=3.0.1,<4.0.0']

setup_kwargs = {
    'name': 'doc-extractor',
    'version': '0.1.1',
    'description': '',
    'long_description': '',
    'author': 'Aditya Varma Uddaraju',
    'author_email': 'adithya951@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
