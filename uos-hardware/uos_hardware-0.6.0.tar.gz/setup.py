# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['uoshardware', 'uoshardware.devices', 'uoshardware.interface']

package_data = \
{'': ['*']}

install_requires = \
['pyserial>=3.5,<4.0']

setup_kwargs = {
    'name': 'uos-hardware',
    'version': '0.6.0',
    'description': 'A hardware abstraction layer for microcontrollers running UOS compliant firmware.',
    'long_description': '# ![NullTek Documentation](https://raw.githubusercontent.com/CreatingNull/NullTek-Assets/main/img/uos/UOSLogoSmall.png) UOS Hardware\n\n[![License](https://img.shields.io/:license-mit-blue.svg)](https://github.com/CreatingNull/UOS-Hardware/blob/main/LICENSE.md)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/uos-hardware?logo=python&logoColor=white)](https://pypi.org/project/uos-hardware/)\n[![PyPI](https://img.shields.io/pypi/v/uos-hardware?logo=pypi&logoColor=white)](https://pypi.org/project/uos-hardware/#history)\n[![Read the Docs](https://img.shields.io/readthedocs/uos-hardware?logo=readthedocs)](https://uos-hardware.nulltek.xyz)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/CreatingNull/UOS-Hardware/main.svg)](https://results.pre-commit.ci/latest/github/CreatingNull/UOS-Hardware/main)\n[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/CreatingNull/uos-hardware/run-tests.yaml?branch=main&label=tests&logo=github)](https://github.com/CreatingNull/UOS-Hardware/actions/workflows/run-tests.yaml)\n\nThis repository contains a hardware abstraction layer for communicating with microcontrollers running UOS compliant firmware.\n\n---\n\nI just do this stuff for fun in my spare time, but feel free to:\n\n[![Support via buymeacoffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/nulltek)\n\n---\n\n## License\n\nThe source of this repo uses the MIT open-source license, for details on the current licensing see [LICENSE](https://github.com/CreatingNull/UOS-Hardware/blob/main/LICENSE.md) or click the badge above.\n',
    'author': 'nulltek',
    'author_email': 'steve.public@nulltek.xyz',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/CreatingNull/UOS-Hardware',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
