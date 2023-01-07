# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pkgs_test', 'pkgs_test.data']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib==3.6.2']

setup_kwargs = {
    'name': 'pkgs-test',
    'version': '0.2.0',
    'description': 'test pkgs ',
    'long_description': '# pkgs_test\n\ntest pkgs \n\n## Installation\n\n```bash\n$ pip install pkgs_test\n```\n\n## Usage\n\n`pkgs_test` can be used to count words in a text file and plot results\nas follows:\n\n```python\nfrom pkgs_test.pkgs_test import count_words\nfrom pkgs_test.plotting import plot_words\nimport matplotlib.pyplot as plt\n\nfile_path = "test.txt"  # path to your file\ncounts = count_words(file_path)\nfig = plot_words(counts, n=10)\nplt.show()\n```\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`pkgs_test` was created by Matthias Heng. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`pkgs_test` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Matthias Heng',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
