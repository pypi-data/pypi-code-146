# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['peakfit']

package_data = \
{'': ['*']}

install_requires = \
['lmfit>=1.1.0,<2.0.0',
 'matplotlib>=3.6.3,<4.0.0',
 'nmrglue>=0.9,<0.10',
 'numpy>=1.24.1,<2.0.0',
 'scipy>=1.10.0,<2.0.0']

entry_points = \
{'console_scripts': ['peakfit = peakfit.peakfit:main',
                     'plot_cest = peakfit.plot_cest:main',
                     'plot_cpmg = peakfit.plot_cpmg:main']}

setup_kwargs = {
    'name': 'peakfit',
    'version': '0.3.2',
    'description': 'PeakFit allow for lineshape fitting in pseudo-3D NMR spectra.',
    'long_description': '## Synopsis\n\nPeakFit allow for lineshape fitting in pseudo-3D NMR spectra.\n',
    'author': 'Guillaume Bouvignies',
    'author_email': 'gbouvignies@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/gbouvignies/PeakFit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
