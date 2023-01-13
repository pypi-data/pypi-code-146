# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['baseten', 'baseten.client_commands', 'baseten.common', 'baseten.models']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.3.0,<10.0.0',
 'click>=7.0',
 'colorama>=0.4.3',
 'coolname>=1.1.0',
 'jinja2>=2.10.3',
 'joblib>=0.12.5',
 'pyyaml>=5.1',
 'requests-toolbelt>=0.9.1,<0.10.0',
 'requests>=2.22',
 'semantic-version>=2.10.0,<3.0.0',
 'single-source>=0.3.0,<0.4.0',
 'tenacity>=8.0.1,<9.0.0',
 'tqdm>=4.62.1,<5.0.0',
 'truss>=0.2.0,<0.3.0',
 'types-pillow>=9.3.0.4,<10.0.0.0',
 'types-pyyaml>=6.0.12.2,<7.0.0.0',
 'types-requests>=2.28.11.7,<3.0.0.0',
 'types-setuptools>=65.6.0.2,<66.0.0.0']

entry_points = \
{'console_scripts': ['baseten = baseten.cli:cli_group']}

setup_kwargs = {
    'name': 'baseten',
    'version': '0.2.18',
    'description': 'Deploy machine learning models to Baseten',
    'long_description': '![Baseten](https://cdn.baseten.co/docs/production/PyPiHeaderBaseten.jpeg)\n\nThis package contains the Python client and CLI for Baseten.\n\nBaseten is an ML Application Builder for data science and machine learning teams. We simplify the set-up of back-ends, front-ends, and MLOps—so your models get used faster. Baseten makes it simple to serve your machine learning models, integrate with custom business logic, and design powerful web apps for business users, all without configuring any infrastructure or writing React or JS. API endpoints, release management, and scalability all come out of the box.\n\nVisit our official documentation at [docs.baseten.co](https://docs.baseten.co).',
    'author': 'Amir Haghighat',
    'author_email': 'amir@baseten.co',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
