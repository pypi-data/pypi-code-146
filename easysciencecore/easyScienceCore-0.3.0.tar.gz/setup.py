# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['easyCore',
 'easyCore.Datasets',
 'easyCore.Fitting',
 'easyCore.Objects',
 'easyCore.Utils',
 'easyCore.Utils.Hugger',
 'easyCore.Utils.io',
 'easyCore.models']

package_data = \
{'': ['*']}

install_requires = \
['asteval>=0.9.27,<0.10.0',
 'bumps>=0.8,<0.10',
 'lmfit>=1.0,<2.0',
 'numpy>=1.21,<2.0',
 'pint>=0.17,<0.19',
 'uncertainties>=3.1,<4.0',
 'xarray>=0.16,<0.21']

extras_require = \
{'ci': ['DFO-LS>=1.2,<2.0',
        'pytest>=7.0.0,<8.0.0',
        'pytest-cov>=3.0.0,<4.0.0',
        'codecov>=2.1.11,<3.0.0',
        'flake8>=5.0,<6.0',
        'tox-gh-actions>=2.11,<3.0'],
 'docs': ['doc8>=0.11.0,<0.12.0',
          'readme-renderer>=35.0,<36.0',
          'Sphinx>=4.0.2,<5.0.0',
          'sphinx-rtd-theme>=1.0.0,<2.0.0',
          'sphinx-autodoc-typehints>=1.12.0,<2.0.0',
          'sphinx-gallery>=0.10.0,<0.11.0'],
 'full': ['DFO-LS>=1.2,<2.0'],
 'test': ['DFO-LS>=1.2,<2.0',
          'pytest>=7.0.0,<8.0.0',
          'pytest-cov>=3.0.0,<4.0.0',
          'codecov>=2.1.11,<3.0.0',
          'flake8>=5.0,<6.0']}

setup_kwargs = {
    'name': 'easysciencecore',
    'version': '0.3.0',
    'description': 'Generic logic for easyScience libraries',
    'long_description': '# [![License][50]][51] [![Release][32]][33] [![Downloads][70]][71] [![CI Build][20]][21] \n\n[![CodeFactor][83]][84] [![Codecov][85]][86]\n[![Lines of code][81]](<>) [![Total lines][80]](<>) [![Files][82]](<>)\n\n\n<img height="80"><img src="https://raw.githubusercontent.com/easyScience/easyCore/master/resources/images/ec_logo.svg" height="65">\n\n**easyCore** is the foundation of the *easyScience* universe, providing the building blocks for libraries and applications which aim to make scientific data simulation and analysis easier.\n\n## Install\n\n**easyCore** can be downloaded using pip:\n\n```pip install easysciencecore```\n\nOr direct from the repository:\n\n```pip install https://github.com/easyScience/easyCore```\n\n## Test\n\nAfter installation, launch the test suite:\n\n```python -m pytest```\n\n## Documentation\n\nDocumentation can be found at:\n\n[https://easyScience.github.io/easyCore](https://easyScience.github.io/easyCore)\n\n## Contributing\nWe absolutely welcome contributions. **easyCore** is maintained by the ESS and on a volunteer basis and thus we need to foster a community that can support user questions and develop new features to make this software a useful tool for all users while encouraging every member of the community to share their ideas.\n\n## License\nWhile **easyCore** is under the BSD-3 license, DFO_LS is subject to the GPL license.\n\n<!---CI Build Status--->\n\n[20]: https://github.com/easyScience/easyCore/workflows/CI%20using%20pip/badge.svg\n\n[21]: https://github.com/easyScience/easyCore/actions\n\n\n<!---Release--->\n\n[32]: https://img.shields.io/pypi/v/easysciencecore?color=green\n\n[33]: https://pypi.org/project/easyScienceCore\n\n\n<!---License--->\n\n[50]: https://img.shields.io/github/license/easyScience/easyCore.svg\n\n[51]: https://github.com/easyScience/easyCore/blob/master/LICENSE.md\n\n\n<!---Downloads--->\n\n[70]: https://img.shields.io/pypi/dm/easyScienceCore.svg\n\n[71]: https://pypi.org/project/easyScienceCore\n\n<!---Code statistics--->\n\n[80]: https://tokei.rs/b1/github/easyScience/easyCore\n\n[81]: https://tokei.rs/b1/github/easyScience/easyCore?category=code\n\n[82]: https://tokei.rs/b1/github/easyScience/easyCore?category=files\n\n[83]: https://www.codefactor.io/repository/github/easyscience/easycore/badge\n\n[84]: https://www.codefactor.io/repository/github/easyscience/easycore\n\n[85]: https://img.shields.io/codecov/c/github/easyScience/easyCore?color=green\n\n[86]: https://app.codecov.io/gh/easyScience/easyCore/',
    'author': 'Simon Ward',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/easyScience/easyCore',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<3.12',
}


setup(**setup_kwargs)
