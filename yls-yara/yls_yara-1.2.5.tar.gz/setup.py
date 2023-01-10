# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yls_yara']

package_data = \
{'': ['*']}

install_requires = \
['yara-python>=4.2.0,<5.0.0', 'yls>=1.1.0,<2.0.0']

entry_points = \
{'yls': ['yara = yls_yara']}

setup_kwargs = {
    'name': 'yls-yara',
    'version': '1.2.5',
    'description': 'YLS plugin adding linting using yara-python.',
    'long_description': '# yls-yara\n\n![PyPI](https://img.shields.io/pypi/v/yls-yara)\n\nAn [YLS](https://www.github.com/avast/yls) plugin adding\n[YARA](https://github.com/VirusTotal/yara) linting capabilities.\n\nThis plugin runs `yara.compile` on every save, parses the errors, and returns\nlist of diagnostic messages.\n\n## License\n\nCopyright (c) 2022 Avast Software, licensed under the MIT license. See the\n[`LICENSE`](https://github.com/avast/yls/blob/master/plugins/yls-yara/LICENSE)\nfile for more details.\n',
    'author': 'Matej Kastak',
    'author_email': 'matej.kastak@avast.com',
    'maintainer': 'Matej Kašťák',
    'maintainer_email': 'matej.kastak@avast.com',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
