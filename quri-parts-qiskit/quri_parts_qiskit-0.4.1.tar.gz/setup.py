# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quri_parts', 'quri_parts.qiskit.circuit']

package_data = \
{'': ['*'], 'quri_parts': ['qiskit/*']}

install_requires = \
['numpy>=1.22.0', 'quri-parts-circuit']

setup_kwargs = {
    'name': 'quri-parts-qiskit',
    'version': '0.4.1',
    'description': 'A plugin to use Qiskit with QURI Parts',
    'long_description': '# QURI Parts Qiskit\n\nQURI Parts Qiskit is a support library for using Qiskit with QURI Parts.\n\n## Documentation\n\n[QURI Parts Documentation](https://quri-parts.qunasys.com)\n\n## Installation\n\n```\npip install quri-parts-qiskit\n```\n\n## License\n\nApache License 2.0\n',
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
