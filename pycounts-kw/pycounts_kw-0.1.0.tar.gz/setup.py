# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pycounts_kw']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.6.2,<4.0.0']

setup_kwargs = {
    'name': 'pycounts-kw',
    'version': '0.1.0',
    'description': 'python package for text loading, cleaning and word counting',
    'long_description': '# pycounts_kw\n\npython package for text loading, cleaning and word counting\n\nDocumentation are available [here](https://pycounts-kw.readthedocs.io/en/latest/)\n\n## Installation\n\n```bash\n$ pip install pycounts_kw\n```\n\n## Usage\n\n`pycounts` can be used to count words in a text file and plot results\nas follows:\n\n```python\nfrom pycounts.pycounts import count_words\nfrom pycounts.plotting import plot_words\nimport matplotlib.pyplot as plt\n\nfile_path = "zen.txt"  # path to your file\ncounts = count_words(file_path)\nfig = plot_words(counts, n=10)\nplt.show()\n```\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`pycounts_kw` was created by kellywujy. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`pycounts_kw` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'kellywujy',
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
