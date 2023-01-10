# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lb', 'lb.nightly.scheduler']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.18,<4.0.0',
 'lb-nightly-configuration>=0.3,<0.4',
 'lb-nightly-db>=0.2,<0.3',
 'lb-nightly-rpc>=0.2,<0.3',
 'lb-nightly-utils>=0.4.1,<0.5.0',
 'luigi>=3.0.3,<4.0.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'lb-nightly-scheduler',
    'version': '0.4.1',
    'description': 'Scheduler implementation for LHCb Nightly and Continuous Integration Build System',
    'long_description': 'None',
    'author': 'Marco Clemencic',
    'author_email': 'marco.clemencic@cern.ch',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.cern.ch/lhcb-core/nightly-builds/lb-nightly-scheduler',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
