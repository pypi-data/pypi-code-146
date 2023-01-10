# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wtforglib']

package_data = \
{'': ['*']}

install_requires = \
['pyyaml>=6.0,<7.0', 'types-pyyaml>=6.0.12.2,<7.0.0.0', 'wheel>=0.38.0,<0.39.0']

setup_kwargs = {
    'name': 'wtforglib',
    'version': '0.4.0',
    'description': 'A set of utility functions I use in my various python projects.',
    'long_description': '# wtforglib\n\n[![Build Status](https://github.com/wtfo-guru/wtforglib/workflows/test/badge.svg?branch=main&event=push)](https://github.com/wtfo-guru/wtforglib/actions?query=workflow%3Atest)\n[![codecov](https://codecov.io/gh/wtfo-guru/wtforglib/branch/main/graph/badge.svg)](https://codecov.io/gh/wtfo-guru/wtforglib)\n[![Python Version](https://img.shields.io/pypi/pyversions/wtforglib.svg)](https://pypi.org/project/wtforglib/)\n[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)\n\nA set of utility functions I use in my various python projects.\n\n## Features\n\n- Fully typed with annotations and checked with mypy, [PEP561 compatible](https://www.python.org/dev/peps/pep-0561/)\n- Add yours!\n\n\n## Installation\n\n```bash\npip install wtforglib\n```\n\n## Documentation\n\n- [Stable](https://wtforglib.readthedocs.io/en/stable)\n\n- [Latest](https://wtforglib.readthedocs.io/en/latest)\n\n## License\n\n[MIT](https://github.com/wtfo-guru/wtforglib/blob/main/LICENSE)\n\n## Credits\n\nThis project was generated with [`wemake-python-package`](https://github.com/wemake-services/wemake-python-package). Current template version is: [5fe13ee2646d5cf38736bacfa8f9dbbfac092efb](https://github.com/wemake-services/wemake-python-package/tree/5fe13ee2646d5cf38736bacfa8f9dbbfac092efb). See what is [updated](https://github.com/wemake-services/wemake-python-package/compare/5fe13ee2646d5cf38736bacfa8f9dbbfac092efb...main) since then.\n',
    'author': 'Quien Sabe',
    'author_email': 'qs5779@mail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/wtfo-guru/wtforglib',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
