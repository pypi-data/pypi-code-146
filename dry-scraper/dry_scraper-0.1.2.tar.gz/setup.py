# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dry_scraper',
 'dry_scraper.data_sources',
 'dry_scraper.data_sources.nhl',
 'dry_scraper.data_sources.nhl.nhl_helpers']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'pandas>=1.4.3,<2.0.0',
 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'dry-scraper',
    'version': '0.1.2',
    'description': 'A framework for retrieving and parsing hockey data into useful forms.',
    'long_description': '# dry_scraper\n\ndocumentation under construction :)',
    'author': 'cak',
    'author_email': 'chris@cak.co',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
