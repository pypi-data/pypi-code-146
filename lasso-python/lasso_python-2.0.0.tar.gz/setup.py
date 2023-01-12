# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lasso',
 'lasso.diffcrash',
 'lasso.dimred',
 'lasso.dimred.sphere',
 'lasso.dimred.svd',
 'lasso.dyna',
 'lasso.femzip',
 'lasso.io',
 'lasso.math',
 'lasso.plotting',
 'lasso.plotting.resources',
 'lasso.utils']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=22.1.0,<23.0.0',
 'h5py>=3.7.0,<4.0.0',
 'matplotlib>=3.6.0,<4.0.0',
 'numpy>=1.23.3,<2.0.0',
 'pandas>=1.5.0,<2.0.0',
 'plotly>=5.10.0,<6.0.0',
 'psutil>=5.9.2,<6.0.0',
 'rich>=12.5.1,<13.0.0',
 'scipy>=1.9.1,<2.0.0',
 'sklearn>=0.0,<0.1']

setup_kwargs = {
    'name': 'lasso-python',
    'version': '2.0.0',
    'description': 'An open-source CAE and Machine Learning library.',
    'long_description': 'None',
    'author': 'open-lasso-python',
    'author_email': 'open.lasso.python@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
