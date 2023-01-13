# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['munitests']

package_data = \
{'': ['*']}

install_requires = \
['ibm-watson>=6.1.0,<7.0.0',
 'jupyter>=1.0.0,<2.0.0',
 'matplotlib>=3.6.3,<4.0.0',
 'notebook>=6.5.2,<7.0.0',
 'pandas>=1.5.2,<2.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'scikit-learn>=1.2.0,<2.0.0',
 'seaborn>=0.12.2,<0.13.0',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'munitests',
    'version': '0.1.0',
    'description': 'A test suite for Chatbot Muni',
    'long_description': '# Munitests\n\nA test suite for the municipal chatbot Muni.\n\nThis package is made with love to support the ongoing development of digitalization in the Danish municipalities. The package contain core functionality\n',
    'author': 'Jens Peder Meldgaard',
    'author_email': 'jenspederm@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
