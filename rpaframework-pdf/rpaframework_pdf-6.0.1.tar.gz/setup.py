# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['RPA', 'RPA.PDF', 'RPA.PDF.keywords']

package_data = \
{'': ['*'], 'RPA.PDF': ['assets/*']}

install_requires = \
['fpdf2>=2.6.0,<3.0.0',
 'pdfminer.six==20221105',
 'pypdf>=3.2.0,<4.0.0',
 'robotframework-pythonlibcore>=4.0.0,<5.0.0',
 'robotframework>=4.0.0,!=4.0.1,<6.0.0',
 'rpaframework-core>=10.0.0,<11.0.0']

setup_kwargs = {
    'name': 'rpaframework-pdf',
    'version': '6.0.1',
    'description': 'PDF library of RPA Framework',
    'long_description': 'rpaframework-pdf\n================\n\nThis library enables various PDF features with `RPA Framework`_\nlibraries, such as locating text by label.\n\n.. _RPA Framework: https://rpaframework.org\n',
    'author': 'RPA Framework',
    'author_email': 'rpafw@robocorp.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://rpaframework.org/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
