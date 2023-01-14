# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mediawiki_scraper']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mediawiki-scraper',
    'version': '0.0.0',
    'description': 'MediaWiki Scraper',
    'long_description': '# MediaWiki Scraper\n\nThis is a placeholder for the project currently titled [`wikiteam3`](https://github.com/elsiehupp/wikiteam3), which will be renamed in order to avoid confusion with the upstream [WikiTeam](https://github.com/WikiTeam/wikiteam/) project.\n',
    'author': 'Elsie Hupp',
    'author_email': 'github@elsiehupp.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
