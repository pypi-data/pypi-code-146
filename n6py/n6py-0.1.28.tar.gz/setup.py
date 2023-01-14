# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['n6py', 'n6py.display', 'n6py.encode', 'n6py.stats']

package_data = \
{'': ['*']}

install_requires = \
['ipython>=8.7.0,<9.0.0', 'numpy>=1.24.1,<2.0.0', 'pandas>=1.5.2,<2.0.0']

setup_kwargs = {
    'name': 'n6py',
    'version': '0.1.28',
    'description': 'Python Power Tools for Scientific Computing, Machine Learning and Deep Learning.',
    'long_description': '&nbsp;\n\n<p align="center">\n  <a href="https://py.n6.ai" target="_blank" rel="noopener noreferrer">\n    <img src="https://raw.githubusercontent.com/n6ai/n6py/main/.github/img/n6py.svg" alt="n6py" width="125" height="auto">\n  </a>\n</p>\n\n# n6py\n\n[![PyPI Latest Release](https://img.shields.io/pypi/v/n6py?color=%23141414&style=for-the-badge)](https://pypi.org/project/n6py)\n[![PyPI Python Version](https://img.shields.io/pypi/pyversions/n6py?color=%23141414&style=for-the-badge)](https://pypi.org/project/n6py)\n\n> ⚡ AI Power Tools\n\nPython Power Tools for Scientific Computing, Machine Learning and Deep Learning.\n\n[Read the Docs to Learn More](https://py.n6.ai).\n\n## Try Online\n\nClick one of the icons to start with a fresh copy of `n6py` in an online environment.\n\n<table>\n  <tbody>\n    <tr>\n      <td>\n        <a href="https://colab.research.google.com/github/n6ai/n6py/blob/main/notebooks/n6py-demo.ipynb">\n          <div align="center">\n            <img width="32" height="32" src="https://raw.githubusercontent.com/n6ai/n6py/main/.github/img/colab.svg" />\n            <div>Colab</div>\n          </div>\n        </a>\n      </td>\n      <td>\n        <a href="https://mybinder.org/v2/git/https%3A%2F%2Fgithub.com%2Fn6ai%2Fn6py/HEAD?labpath=%2Fnotebooks%2Fn6py-demo.ipynb">\n          <div align="center">\n            <img width="32" height="32" src="https://raw.githubusercontent.com/n6ai/n6py/main/.github/img/binder.svg" />\n            <div>Binder</div>\n          </div>\n        </a>\n      </td>\n      <td>\n        <a href="https://kaggle.com/kernels/welcome?src=https://github.com/n6ai/n6py/blob/main/notebooks/n6py-demo.ipynb">\n          <div align="center">\n            <img width="62" height="32" src="https://raw.githubusercontent.com/n6ai/n6py/main/.github/img/kaggle.svg" />\n            <div>Kaggle</div>\n          </div>\n        </a>\n      </td>\n    </tr>\n  </tbody>\n</table>\n\n## Features\n\n- 🐍 Python - Utility library for AI Python projects.\n- 📃 Jupyter Notebooks - Designed for use inside Jupyter Notebooks but also works in regular .py files.\n- ☁️ Cloud - Notebook Cloud Environment compatible e.g. Google Colab.\n- 👶 Simple - Dive right in by adding n6py package to your project via pip.\n- 📦 Modular - Pick and choose which modules to import to suit your needs.\n- 🎲 Framework Agnostic - Use n6py with many common frameworks - NumPy, Pandas, etc ...\n\n## Installation\n\n```sh\npip install n6py\n```\n\n## Import\n\n```py\nimport n6py as n6\n```\n\n## Contribution\n\nSee [Contributing Guide](https://github.com/n6ai/n6py/blob/main/.github/CONTRIBUTING.md).\n\n## License\n\nMIT\n',
    'author': 'Sergej Samsonenko',
    'author_email': 'contact@sergej.codes',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://py.n6.ai',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
