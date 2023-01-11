# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['formkit_ninja',
 'formkit_ninja.management.commands',
 'formkit_ninja.migrations']

package_data = \
{'': ['*'], 'formkit_ninja': ['samples/*']}

install_requires = \
['Django>=4.1.5,<5.0.0',
 'django-ninja>=0.20.0,<0.21.0',
 'django-ordered-model>=3.6,<4.0',
 'pydantic<2']

setup_kwargs = {
    'name': 'formkit-ninja',
    'version': '0.1.0',
    'description': 'A Django-Ninja backend to specify FormKit schemas',
    'long_description': '# Formkit-Ninja\n\nA Django-Ninja framework for FormKit schemas and form submissions\n',
    'author': 'Josh Brooks',
    'author_email': 'josh@catalpa.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
