# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lifeomic_patient_ml_types']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'lifeomic-patient-ml-types',
    'version': '2.0.2',
    'description': 'Shared types for the patient-ml-service repos.',
    'long_description': 'None',
    'author': 'LifeOmic',
    'author_email': 'development@lifeomic.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
