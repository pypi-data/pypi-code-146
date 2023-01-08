# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_bpm']

package_data = \
{'': ['*']}

install_requires = \
['PyWavelets>=1.4.1,<2.0.0', 'numpy>=1.24.1,<2.0.0', 'scipy>=1.10.0,<2.0.0']

entry_points = \
{'console_scripts': ['bpm-rename = python_bpm.app:main']}

setup_kwargs = {
    'name': 'bpm-renamer',
    'version': '0.3.0',
    'description': '',
    'long_description': 'BPM Detector in Python\n=======================\nImplementation of a Beats Per Minute (BPM) detection algorithm, as presented in the paper of G. Tzanetakis, G. Essl and P. Cook titled: "Audio Analysis using the Discrete Wavelet Transform".\n\nYou can find it here: http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.63.5712\n\nBased on the work done in the MATLAB code located at github.com/panagiop/the-BPM-detector-python.\n\nProcess .wav file to determine the Beats Per Minute.\n\nDependencies: scipy, numpy, pywavelets, matplotlib\n\n',
    'author': 'Bruce Collie',
    'author_email': 'brucecollie82@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<3.12',
}


setup(**setup_kwargs)
