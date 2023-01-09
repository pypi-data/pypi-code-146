# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['entente', 'entente.landmarks']

package_data = \
{'': ['*']}

install_requires = \
['cached_property',
 'lacecore[obj]>=3.0.0a0,<4',
 'numpy',
 'ounce>=1.1.1,<2.0',
 'polliwog>=3.0.0a0,<4',
 'simplejson',
 'tqdm',
 'vg>=2.0.0']

extras_require = \
{'cli': ['click>7.0,<9.0', 'PyYAML>=5.1', 'tri-again>=2.0.0a0,<3'],
 'landmarker': ['proximity>=2.0.0,<3', 'scipy'],
 'meshlab': ['meshlab-pickedpoints>=4.1.0,<5'],
 'surface-regressor': ['proximity>=2.0.0,<3', 'scipy']}

setup_kwargs = {
    'name': 'entente',
    'version': '3.0.0a2',
    'description': 'Polygonal meshes in vertex-wise correspondence',
    'long_description': 'None',
    'author': 'Paul Melnikow',
    'author_email': 'github@paulmelnikow.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/lace/entente',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
