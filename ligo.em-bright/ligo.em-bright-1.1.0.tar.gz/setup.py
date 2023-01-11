# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ligo', 'ligo.em_bright', 'ligo.em_bright.tests']

package_data = \
{'': ['*'], 'ligo.em_bright.tests': ['data/*']}

install_requires = \
['astropy>=5.2.1',
 'h5py>=3.7.0',
 'lalsuite>=7.0,<8.0',
 'pandas>=1.5.2',
 'scikit-learn==1.1.3']

entry_points = \
{'console_scripts': ['em_bright_categorize = ligo.em_bright.categorize:main',
                     'em_bright_categorize_all_eos = '
                     'ligo.em_bright.categorize:main_all',
                     'em_bright_create_param_sweep_plot = '
                     'ligo.em_bright.utils:param_sweep_plot',
                     'em_bright_dag_writer = ligo.em_bright.dag_writer:main',
                     'em_bright_extract = ligo.em_bright.utils:extract',
                     'em_bright_join = ligo.em_bright.utils:join',
                     'em_bright_train = ligo.em_bright.utils:train']}

setup_kwargs = {
    'name': 'ligo.em-bright',
    'version': '1.1.0',
    'description': 'Possibility and properties of Electromagnetically-bright sources of gravitational-wave events',
    'long_description': '# ligo.em_bright\n\nThis library provides the tools to compute the possibility of merging gravitational-wave binaries to have an electromagnetic counterpart or having a component in the lower mass-gap region. The data products are source properties\n- `HasNS`: The mass of at least one of the compact binary coalescence is consistent with a neutron star.\n- `HasRemnant`: A non-zero amount of remnant matter remained outside the final compact object (a necessary but not sufficient condition to produce certain kinds of electromagnetic emission such as a short GRB or a kilonova).\n- `HasMassGap`: The mass of at least one of the compact binary coalescence is consistent with lower mass-gap region i.e. between 3-5 solar mass.\n\nThe `HasNS` and `HasRemnant` quantities depend on, and are marginalized over, several neutron star equations of state (EOS). The marginalization is done using data from [GW170817](https://www.gw-openscience.org/eventapi/html/GWTC-1-confident/GW170817/).\n',
    'author': 'Deep Chatterjee',
    'author_email': 'deep.chatterjee@ligo.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
