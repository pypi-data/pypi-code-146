# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['infoml', 'infoml.data']

package_data = \
{'': ['*']}

install_requires = \
['biopython>=1.80,<2.0',
 'geoparse>=2.0.3,<3.0.0',
 'numpy>=1.24.1,<2.0.0',
 'pandas>=1.5.2,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'rich>=13.0.0,<14.0.0',
 'scikit-learn>=1.2.0,<2.0.0',
 'scipy>=1.9.3,<2.0.0',
 'seaborn>=0.12.2,<0.13.0',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'infoml',
    'version': '0.4.0',
    'description': 'Python package for bioinformatics analysis and machine learning.',
    'long_description': '<h1 align="center">infoml</h1>\n\n<p align="center">\n<a href="https://github.com/psf/black/blob/main/LICENSE">\n    <img alt="License: MIT" src="https://img.shields.io/github/license/Kabilan108/infoml">\n</a>\n<a href="https://github.com/psf/black">\n    <img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">\n</a>\n<a href="https://codecov.io/gh/Kabilan108/infoml" >\n    <img src="https://codecov.io/gh/Kabilan108/infoml/branch/main/graph/badge.svg?token=38Y14PAAQQ"/>\n</a>\n<a href="https://github.com/Kabilan108/infoml/actions/workflows/CI-CD.yml">\n    <img alt="Test Status" src="https://github.com/Kabilan108/infoml/actions/workflows/CI-CD.yml/badge.svg?branch=main">\n</a>\n<a href="https://wakatime.com/badge/user/6a085912-85f1-47f5-acc7-c7f5ac1110ab/project/51ef67da-2e82-431e-9dc9-9bdd6d1c3d48">\n    <img\n    src="https://wakatime.com/badge/user/6a085912-85f1-47f5-acc7-c7f5ac1110ab/project/51ef67da-2e82-431e-9dc9-9bdd6d1c3d48.svg"\n    alt="wakatime">\n</a>\n</p>\n\nPython package for bioinformatics analysis and machine learning.\n\n## Installation\n\n```bash\npip install infoml\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note\nthat this project is released with a Code of Conduct. By contributing to this\nproject, you agree to abide by its terms.\n\n## License\n\n`infoml` was created by Tony Kabilan Okeke. It is licensed under the terms of\nthe MIT license.\n\n## Credits\n\n`infoml` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/)\nand the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Tony Kabilan Okeke',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
