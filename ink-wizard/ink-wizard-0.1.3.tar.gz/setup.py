# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ink_wizard', 'ink_wizard.commands', 'ink_wizard.template_generators']

package_data = \
{'': ['*'],
 'ink_wizard': ['templates/flipper/*',
                'templates/psp22/*',
                'templates/psp34/*',
                'templates/psp37/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0', 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['ink-wizard = ink_wizard.main:main']}

setup_kwargs = {
    'name': 'ink-wizard',
    'version': '0.1.3',
    'description': 'Ink Wizard is a CLI tool used to scaffold Flipper, PSP-22, PSP-34, PSP-37 smart contracts. CLI will ask user on what kind of functionality user needs. It will scaffold smart contracts based on user options.',
    'long_description': '# Ink Wizard\n\nInk Wizard is a CLI tool used to scaffold Flipper, PSP-22, PSP-34, PSP-37 smart contracts. CLI will ask user on what kind of functionality user needs. It will scaffold smart contracts based on user options.\n',
    'author': 'Aviraj Khare',
    'author_email': 'thisisavirajkhare@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
