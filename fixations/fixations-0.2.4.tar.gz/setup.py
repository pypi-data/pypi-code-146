# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fixations']

package_data = \
{'': ['*'],
 'fixations': ['fix_repository_2010_edition_20200402/*',
               'fix_repository_2010_edition_20200402/FIX.4.0/Base/*',
               'fix_repository_2010_edition_20200402/FIX.4.1/Base/*',
               'fix_repository_2010_edition_20200402/FIX.4.2/*',
               'fix_repository_2010_edition_20200402/FIX.4.2/Base/*',
               'fix_repository_2010_edition_20200402/FIX.4.3/Base/*',
               'fix_repository_2010_edition_20200402/FIX.4.4/Base/*',
               'fix_repository_2010_edition_20200402/FIX.5.0/Base/*',
               'fix_repository_2010_edition_20200402/FIX.5.0SP1/Base/*',
               'fix_repository_2010_edition_20200402/FIX.5.0SP2/Base/*',
               'fix_repository_2010_edition_20200402/FIXT.1.1/Base/*',
               'fix_repository_2010_edition_20200402/Unified/*',
               'fix_repository_2010_edition_20200402/schema/*',
               'fix_repository_2010_edition_20200402/xsl/*',
               'templates/*']}

install_requires = \
['dataclasses-json>=0.5.7,<0.6.0',
 'flask>=2.2.2,<3.0.0',
 'gunicorn>=20.1.0,<21.0.0',
 'pytest>=7.2.0,<8.0.0',
 'tabulate>=0.9.0,<0.10.0',
 'termcolor>=2.1.1,<3.0.0',
 'urwid>=2.1.2,<3.0.0']

entry_points = \
{'console_scripts': ['fix_parse_log = fixations.fix_parse_log:main',
                     'fix_tags = fixations.fix_tags:main',
                     'webfix = fixations.webfix:main']}

setup_kwargs = {
    'name': 'fixations',
    'version': '0.2.4',
    'description': 'This is a set of tools to look up / visualize FIX protocol data',
    'long_description': "# FIXations!\n## A set of tools to handle FIX protocol data\n - **fix_tags.py** - _explore FIX tags and their associated values either as CLI output or a GUI-like textual interface_\n - **fix_parse_log.py** - _extract FIX lines from a (log) file and present them in a nicely formatted grid_\n - **webfix.py** - _present copy-n-paste'd FIX lines into a nicely formatted grid_\n\n### Examples\n#### fix_tags.py\n#### fix_parse_log.py\n#### webfix.py\n\n### Installation\n\n### How to run them\n\n\n## FIX reference data source\nThe data is extracted from the FIX specs available here: \n\n> https://www.fixtrading.org/packages/fix-repository-2010/ \n(see fix_repository_2010_edition_20200402.zip).\n\nNOTE: it requires the creation of a login/password to access it.\n",
    'author': 'Jerome Provensal',
    'author_email': 'jeromegit@provensal.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/jeromegit/fixations',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
