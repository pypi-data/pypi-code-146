# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stock_summary']

package_data = \
{'': ['*'],
 'stock_summary': ['demo_datasets/*', 'html_files/*', 'init_datasets/*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'jinja2>=3.1.2,<4.0.0',
 'pandas>=1.5.2,<2.0.0',
 'plotly>=5.11.0,<6.0.0',
 'requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['stock_summary_tool = stock_summary.main:main']}

setup_kwargs = {
    'name': 'stock-summary-tool',
    'version': '0.1.0',
    'description': 'Tool for tracking of your investments and your actual portfolio',
    'long_description': 'DEMO\n2. Create virtual environment that you will use for the project and activate it (python3.8+ required):\n   1. **python3 -m venv my_venv/**\n   2. **source my_venv/bin/activate**\n2. Install the package \n   1. **pip3 install stock_summary_tool**\n3. Go to https://rapidapi.com and log in.\n4. Go to https://rapidapi.com/sparior/api/yahoo-finance15/ and obtain your API key.\n5. Save your key for the project:\n   1. **stock_summary_tool save-token <YOUR_TOKEN>**\n\n\n',
    'author': 'Simon Foucek',
    'author_email': 'foucek.simon@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
