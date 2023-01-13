# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['easyCrystallography',
 'easyCrystallography.Components',
 'easyCrystallography.Elements',
 'easyCrystallography.Structures',
 'easyCrystallography.Symmetry',
 'easyCrystallography.io',
 'easyCrystallography.io.cif']

package_data = \
{'': ['*'], 'easyCrystallography': ['Databases/*']}

install_requires = \
['easysciencecore>=0.3.0,<0.4.0',
 'gemmi>=0.5.8,<0.6.0',
 'periodictable>=1.6.1,<2.0.0']

extras_require = \
{'docs': ['doc8>=0.11.0,<0.12.0',
          'readme-renderer>=35,<38',
          'Sphinx>=4.0.2,<6.0.0',
          'sphinx-rtd-theme>=1.0.0,<2.0.0',
          'sphinx-autodoc-typehints>=1.12.0,<2.0.0',
          'sphinx-gallery>=0.10,<0.12'],
 'test': ['pytest>=7.0.0,<8.0.0',
          'pytest-cov>=3,<5',
          'codecov>=2.1.11,<3.0.0',
          'flake8>=5.0,<6.0']}

setup_kwargs = {
    'name': 'easycrystallography',
    'version': '0.2.1',
    'description': 'Crystallography in easyScience',
    'long_description': '# [![License][50]][51] [![Release][32]][33] [![Downloads][70]][71] [![CI Build][20]][21] \n\n[![CodeFactor][83]][84] [![Codecov][85]][86]\n[![Lines of code][81]](<>) [![Total lines][80]](<>) [![Files][82]](<>)\n\n<img height="80"><img src="https://raw.githubusercontent.com/easyScience/easyCrystallography/develop/resources/images/ec_logo.svg" height="65">\n\n**easyCrystallography** is a library that can be used for the generation and manipulation of crystal structures.\n\n## Install\n\n**easyCrystallography** can be downloaded using pip:\n\n```pip install easyCrystallography```\n\nOr direct from the repository:\n\n```pip install https://github.com/easyScience/easyCrystallography```\n\n## Test\n\nAfter installation, launch the test suite:\n\n```python -m pytest```\n\n[//]: # (## Documentation)\n\n[//]: # ()\n[//]: # (Documentation can be found at:)\n\n[//]: # ()\n[//]: # ([https://easyScience.github.io/easyCore]&#40;https://easyScience.github.io/easyCore&#41;)\n\n## Contributing\nWe absolutely welcome contributions. **easyCore** is maintained by the ESS and on a volunteer basis and thus we need to foster a community that can support user questions and develop new features to make this software a useful tool for all users while encouraging every member of the community to share their ideas.\n\n## License\nWhile **easyCore** is under the BSD-3 license\n\n<!---CI Build Status--->\n\n[20]: https://github.com/easyScience/easyCrystallography/workflows/CI%20using%20pip/badge.svg\n\n[21]: https://github.com/easyScience/easyCrystallography/actions\n\n\n<!---Release--->\n\n[32]: https://img.shields.io/pypi/v/easysciencecore?color=green\n\n[33]: https://pypi.org/project/easyCrystallography\n\n\n<!---License--->\n\n[50]: https://img.shields.io/github/license/easyScience/easyCrystallography.svg\n\n[51]: https://github.com/easyScience/easyCrystallography/blob/master/LICENSE.md\n\n\n<!---Downloads--->\n\n[70]: https://img.shields.io/pypi/dm/easyCrystallography.svg\n\n[71]: https://pypi.org/project/easyCrystallography\n\n<!---Code statistics--->\n\n[80]: https://tokei.rs/b1/github/easyScience/easyCrystallography\n\n[81]: https://tokei.rs/b1/github/easyScience/easyCrystallography?category=code\n\n[82]: https://tokei.rs/b1/github/easyScience/easyCrystallography?category=files\n\n[83]: https://www.codefactor.io/repository/github/easyscience/easyCrystallography/badge\n\n[84]: https://www.codefactor.io/repository/github/easyscience/easyCrystallography\n\n[85]: https://img.shields.io/codecov/c/github/easyScience/easyCrystallography?color=green\n\n[86]: https://app.codecov.io/gh/easyScience/easyCrystallography/\n',
    'author': 'Simon Ward',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/easyScience/easyCrystallography',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<=3.12',
}


setup(**setup_kwargs)
