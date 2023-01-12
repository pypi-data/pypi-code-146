# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quri_parts',
 'quri_parts.circuit',
 'quri_parts.circuit.noise',
 'quri_parts.circuit.topology',
 'quri_parts.circuit.transpile']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22.0', 'typing-extensions>=4.1.1,<5.0.0']

setup_kwargs = {
    'name': 'quri-parts-circuit',
    'version': '0.4.1',
    'description': 'Platform-independent quantum circuit library',
    'long_description': '# QURI Parts Circuit\n\nQURI Parts Circuit is a platform-independent quantum circuit library.\n\n## Documentation\n\n[QURI Parts Documentation](https://quri-parts.qunasys.com)\n\n## Installation\n\n```\npip install quri-parts-circuit\n```\n\n## License\n\nApache License 2.0\n',
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
