# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quri_parts',
 'quri_parts.stim',
 'quri_parts.stim.circuit',
 'quri_parts.stim.estimator',
 'quri_parts.stim.operator',
 'quri_parts.stim.sampler']

package_data = \
{'': ['*']}

install_requires = \
['quri-parts-circuit', 'quri-parts-core', 'stim>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'quri-parts-stim',
    'version': '0.4.1',
    'description': 'A plugin to use Stim with QURI Parts',
    'long_description': '# QURI Parts Stim\n\nQURI Parts Stim is a support library for using Stim with QURI Parts.\nYou can combine your code written in QURI Parts with this library to execute it on Stim.\n\n## Documentation\n\n[QURI Parts Documentation](https://quri-parts.qunasys.com)\n\n## Installation\n\n```\npip install quri-parts-stim\n```\n\n## License\n\nApache License 2.0\n',
    'author': 'QURI Parts Authors',
    'author_email': 'opensource@qunasys.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/QunaSys/quri-parts',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.8,<4.0.0',
}


setup(**setup_kwargs)
