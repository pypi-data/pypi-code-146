# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quri_parts',
 'quri_parts.braket',
 'quri_parts.braket.backend',
 'quri_parts.braket.circuit']

package_data = \
{'': ['*']}

install_requires = \
['amazon-braket-sdk>=1.25.1,<2.0.0',
 'quri-parts-circuit',
 'quri-parts-core',
 'typing-extensions>=4.1.1,<5.0.0']

setup_kwargs = {
    'name': 'quri-parts-braket',
    'version': '0.4.1',
    'description': 'A plugin to use Amazon Braket SDK with QURI Parts',
    'long_description': '# QURI Parts Braket\n\nQURI Parts Braket is a support library for using Amazon Braket SDK with QURI Parts.\nYou can combine your code written in QURI Parts with this library to execute it on Amazon Braket.\n\n## Documentation\n\n[QURI Parts Documentation](https://quri-parts.qunasys.com)\n\n## Installation\n\n```\npip install quri-parts-braket\n```\n\n## License\n\nApache License 2.0\n',
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
