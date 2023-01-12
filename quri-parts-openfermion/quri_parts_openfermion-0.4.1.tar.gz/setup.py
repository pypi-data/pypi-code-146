# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quri_parts',
 'quri_parts.openfermion',
 'quri_parts.openfermion.operator',
 'quri_parts.openfermion.transforms']

package_data = \
{'': ['*']}

install_requires = \
['openfermion>=1.5.1,<2.0.0',
 'quri-parts-chem',
 'quri-parts-core',
 'typing-extensions>=4.1.1,<5.0.0']

setup_kwargs = {
    'name': 'quri-parts-openfermion',
    'version': '0.4.1',
    'description': 'A support library for using OpenFermion with QURI Parts',
    'long_description': '# QURI Parts OpenFermion\n\nQURI Parts OpenFermion is a support library for using OpenFermion with QURI Parts.\n\n## Documentation\n\n[QURI Parts Documentation](https://quri-parts.qunasys.com)\n\n## Installation\n\n```\npip install quri-parts-openfermion\n```\n\n## License\n\nApache License 2.0\n',
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
