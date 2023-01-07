# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['xztrainer', 'xztrainer.engine', 'xztrainer.logger']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22.1', 'tqdm>=4.62.3']

extras_require = \
{'deepspeed:sys_platform == "linux"': ['deepspeed>=0.5.10'],
 'tensorboard': ['tensorboard>=2.8.0'],
 'torch': ['torch>=1.10.0']}

setup_kwargs = {
    'name': 'xztrainer',
    'version': '0.3.5',
    'description': 'A customizable training pipeline for PyTorch',
    'long_description': 'None',
    'author': 'Maxim Afanasyev',
    'author_email': 'mr.applexz@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
