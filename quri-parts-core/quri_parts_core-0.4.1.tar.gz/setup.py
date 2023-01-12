# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quri_parts',
 'quri_parts.backend',
 'quri_parts.core',
 'quri_parts.core.circuit',
 'quri_parts.core.estimator',
 'quri_parts.core.estimator.sampling',
 'quri_parts.core.measurement',
 'quri_parts.core.operator',
 'quri_parts.core.operator.grouping',
 'quri_parts.core.operator.representation',
 'quri_parts.core.sampling',
 'quri_parts.core.state',
 'quri_parts.core.utils']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22.0', 'quri-parts-circuit', 'typing-extensions>=4.1.1,<5.0.0']

setup_kwargs = {
    'name': 'quri-parts-core',
    'version': '0.4.1',
    'description': 'A platform-independent library for quantum computing',
    'long_description': '# QURI Parts Core\n\nQURI Parts Core is a core component of QURI Parts, a platform-independent library for quantum computing.\n\n## Documentation\n\n[QURI Parts Documentation](https://quri-parts.qunasys.com)\n\n## Installation\n\n```\npip install quri-parts-core\n```\n\n## License\n\nApache License 2.0\n',
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
