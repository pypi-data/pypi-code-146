# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['signialib']

package_data = \
{'': ['*'],
 'signialib': ['calibrations/001/Ferraris/2022-07-24_16-00/*',
               'calibrations/002/Ferraris/2022-07-24_16-00/*']}

install_requires = \
['joblib>=1.0.0,<2.0.0',
 'nilspodlib>=3.2.2,<4.0.0',
 'numpy>=1',
 'pandas>=1,<2',
 'scipy>=1.6.1,<2.0.0']

setup_kwargs = {
    'name': 'signialib',
    'version': '1.2.0',
    'description': 'Data handling of the IMUs integrated into Signia hearing aids',
    'long_description': 'None',
    'author': 'Ann-Kristin Seifer',
    'author_email': 'ann-kristin.seifer@fau.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
