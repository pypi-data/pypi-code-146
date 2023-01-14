# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['isaac_xml_validator']
entry_points = \
{'console_scripts': ['isaac-xml-validator = isaac_xml_validator:main']}

setup_kwargs = {
    'name': 'isaac-xml-validator',
    'version': '1.1.0',
    'description': 'A script to validate XML files for The Binding of Isaac: Rebirth',
    'long_description': 'None',
    'author': 'Wofsauge',
    'author_email': 'jan-.-@t-online.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
