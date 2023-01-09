# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ipp_toolkit',
 'ipp_toolkit.data',
 'ipp_toolkit.experiments',
 'ipp_toolkit.planners',
 'ipp_toolkit.predictors',
 'ipp_toolkit.sensors',
 'ipp_toolkit.trainers.model_based',
 'ipp_toolkit.utils',
 'ipp_toolkit.utils.optimization',
 'ipp_toolkit.utils.rl',
 'ipp_toolkit.utils.rl.agents',
 'ipp_toolkit.visualization',
 'ipp_toolkit.world_models']

package_data = \
{'': ['*']}

install_requires = \
['gpytorch>=1.8.1,<2.0.0',
 'gym>=0.21,<0.22',
 'imagecodecs>=2022.9.26,<2023.0.0',
 'imitation>=0.3.2,<0.4.0',
 'matplotlib>=3.5.3,<4.0.0',
 'moviepy>=1.0.3,<2.0.0',
 'numpy>=1.23.2,<2.0.0',
 'planetary-computer>=0.4.9,<0.5.0',
 'platypus-opt>=1.1.0,<2.0.0',
 'pymongo>=4.2.0,<5.0.0',
 'pystac>=1.6.1,<2.0.0',
 'python-tsp>=0.3.1,<0.4.0',
 'rioxarray>=0.13.3,<0.14.0',
 'sacred[mongodb]>=0.8.2,<0.9.0',
 'scikit-image>=0.19.3,<0.20.0',
 'scipy>=1.9.0,<2.0.0',
 'sklearn>=0.0,<0.1',
 'stable-baselines3[extra]>=1.6.2,<2.0.0',
 'torchgeo>=0.3.1,<0.4.0',
 'ubelt>=1.2.1,<2.0.0']

setup_kwargs = {
    'name': 'ipp-toolkit',
    'version': '0.1.0',
    'description': 'A general framework for informative path planning experiments, with a focus on wrapping datasets, sensors, planners, and visualization in a modular manner',
    'long_description': 'None',
    'author': 'David Russell',
    'author_email': 'davidrussell327@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
