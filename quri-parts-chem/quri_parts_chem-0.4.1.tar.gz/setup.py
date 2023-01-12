# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quri_parts', 'quri_parts.chem.transforms']

package_data = \
{'': ['*'], 'quri_parts': ['chem/*']}

install_requires = \
['quri-parts-core', 'typing-extensions>=4.1.1,<5.0.0']

setup_kwargs = {
    'name': 'quri-parts-chem',
    'version': '0.4.1',
    'description': 'Quantum computer algorithms for chemistry',
    'long_description': '# QURI Parts Chem\n\nQURI Parts Chem is a library containing implementations of quantum computer algorithms for chemistry.\n\n## Documentation\n\n[QURI Parts Documentation](https://quri-parts.qunasys.com)\n\n## Installation\n\n```\npip install quri-parts-chem\n```\n\n## License\n\nApache License 2.0\n',
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
