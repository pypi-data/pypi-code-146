# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quri_parts',
 'quri_parts.algo',
 'quri_parts.algo.ansatz',
 'quri_parts.algo.mitigation',
 'quri_parts.algo.mitigation.clifford_data_regression',
 'quri_parts.algo.mitigation.readout_mitigation',
 'quri_parts.algo.mitigation.zero_noise_extrapolation',
 'quri_parts.algo.optimizer',
 'quri_parts.algo.utils']

package_data = \
{'': ['*']}

install_requires = \
['quri-parts-circuit',
 'quri-parts-core',
 'scipy>=1.9.1,<2.0.0',
 'typing-extensions>=4.1.1,<5.0.0']

setup_kwargs = {
    'name': 'quri-parts-algo',
    'version': '0.4.1',
    'description': 'Algorithms for quantum computers',
    'long_description': '# QURI Parts Algo\n\nQURI Parts Algo is a library containing implementations of algorithms for quantum computers.\n\n## Documentation\n\n[QURI Parts Documentation](https://quri-parts.qunasys.com)\n\n## Installation\n\n```\npip install quri-parts-algo\n```\n\n## License\n\nApache License 2.0\n',
    'author': 'QURI Parts Authors',
    'author_email': 'opensource@qunasys.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/QunaSys/quri-parts',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.8,<3.12',
}


setup(**setup_kwargs)
