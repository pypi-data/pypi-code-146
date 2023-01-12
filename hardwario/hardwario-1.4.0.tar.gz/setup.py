# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hardwario', 'hardwario.hardwario']

package_data = \
{'': ['*']}

install_requires = \
['hardwario-chester>=v1.24.0', 'hardwario-cloud>=1.4.2']

setup_kwargs = {
    'name': 'hardwario',
    'version': '1.4.0',
    'description': 'HARDWARIO Command Line Tool',
    'long_description': '<a href="https://www.hardwario.com/"><img src="https://www.hardwario.com/ci/assets/hw-logo.svg" width="200" alt="HARDWARIO Logo" align="right"></a>\n\n# HARDWARIO CLI Tools\n\n[![Main](https://github.com/hardwario/py-hardwario/actions/workflows/main.yaml/badge.svg)](https://github.com/hardwario/py-hardwario/actions/workflows/main.yaml)\n[![Release](https://img.shields.io/github/release/hardwario/py-hardwario.svg)](https://github.com/hardwario/py-hardwario/releases)\n[![PyPI](https://img.shields.io/pypi/v/hardwario.svg)](https://pypi.org/project/hardwario/)\n[![License](https://img.shields.io/github/license/hardwario/py-hardwario.svg)](https://github.com/hardwario/py-hardwario/blob/master/LICENSE)\n[![Twitter](https://img.shields.io/twitter/follow/hardwario_en.svg?style=social&label=Follow)](https://twitter.com/hardwario_en)\n\nThis repository contains Python package [hardwario](https://pypi.org/project/hardwario/)\n\n\n## License\n\nThis project is licensed under the [MIT License](https://opensource.org/licenses/MIT/) - see the [LICENSE](LICENSE) file for details.\n\n---\n\nMade with &#x2764;&nbsp; by [**HARDWARIO a.s.**](https://www.hardwario.com/) in the heart of Europe.\n',
    'author': 'Karel Blavka',
    'author_email': 'karel.blavka@hardwario.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/hardwario/py-hardwario',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
