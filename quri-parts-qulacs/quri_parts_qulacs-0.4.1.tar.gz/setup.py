# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quri_parts',
 'quri_parts.qulacs',
 'quri_parts.qulacs.circuit',
 'quri_parts.qulacs.circuit.noise',
 'quri_parts.qulacs.operator']

package_data = \
{'': ['*']}

install_requires = \
['Qulacs>=0.3.0,<0.6.0',
 'quri-parts-circuit',
 'quri-parts-core',
 'typing-extensions>=4.1.1,<5.0.0']

setup_kwargs = {
    'name': 'quri-parts-qulacs',
    'version': '0.4.1',
    'description': 'A plugin to use Qulacs with QURI Parts',
    'long_description': '# QURI Parts Qulacs\n\nQURI Parts Qulacs is a support library for using Qulacs with QURI Parts.\nYou can combine your code written in QURI Parts with this library to execute it on Qulacs.\n\n## Documentation\n\n[QURI Parts Documentation](https://quri-parts.qunasys.com)\n\n## Installation\n\n```\npip install quri-parts-qulacs\n```\n\n## License\n\nApache License 2.0\n',
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
