# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['security_commons',
 'security_commons.common',
 'security_commons.common.reporting']

package_data = \
{'': ['*'],
 'security_commons.common.reporting': ['templates/*', 'templates/assets/*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'cvss>=2.5,<3.0',
 'hoppr-cyclonedx-models>=0.2.1,<0.3.0',
 'packageurl-python>=0.10.1,<0.11.0',
 'rich>=12.5.1,<13.0.0',
 'tabulate>=0.9.0,<0.10.0',
 'tinydb>=4.7.0,<5.0.0',
 'typer>=0.7.0,<0.8.0']

setup_kwargs = {
    'name': 'hoppr-security-commons',
    'version': '0.0.6',
    'description': 'Common Library For hoppr-cop',
    'long_description': 'None',
    'author': 'kganger',
    'author_email': 'keith.e.ganger@lmco.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
