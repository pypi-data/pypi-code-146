# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pycounts_lennonay']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.4.3']

setup_kwargs = {
    'name': 'pycounts-lennonay',
    'version': '0.1.0',
    'description': 'Calculate word counts in a text file!',
    'long_description': '# pycounts_lennonay\n\nCalculate word counts in a text file!\n\n## Installation\n\n```bash\n$ pip install pycounts_lennonay\n```\n\n## Usage\n\n`pycounts_lennonay` can be used to count words in a text file and plot results\nas follows:\n\n```python\nfrom pycounts_lennonay.pycounts_lennonay import count_words\nfrom pycounts_lennonay.plotting import plot_words\nimport matplotlib.pyplot as plt\n\nfile_path = "test.txt"  # path to your file\ncounts = count_words(file_path)\nfig = plot_words(counts, n=10)\nplt.show()\n```\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`pycounts_lennonay` was created by Lennon Au-Yeung. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`pycounts_lennonay` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Lennon Au-Yeung',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
