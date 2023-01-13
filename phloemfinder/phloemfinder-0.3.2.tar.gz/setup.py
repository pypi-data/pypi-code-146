# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['phloemfinder']

package_data = \
{'': ['*']}

install_requires = \
['TPOT>=0.11.7', 'pandas>=1.5.1', 'scikit-learn>=0.24.1', 'seaborn>=0.12.1']

setup_kwargs = {
    'name': 'phloemfinder',
    'version': '0.3.2',
    'description': 'Find plant metabolites related to whitefly pest resistance',
    'long_description': '# phloemfinder\n\nFind plant metabolites related to whitefly pest resistance\n\n## Installation\n\n```bash\n$ pip install phloemfinder\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`phloemfinder` was created by Lissy-Anne Denkers and Marc Galland. It is licensed under the terms of the Apache License 2.0 license.\n\n## Credits\n\n`phloemfinder` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n\n## Useful reading\n\n- [Autosklearn talks](https://github.com/automl/auto-sklearn-talks)\n- [Numpy docstring examples](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html#example-numpy)',
    'author': 'Marc Galland',
    'author_email': 'm.galland@uva.nl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/BleekerLab/phloemfinder',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
