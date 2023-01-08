# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['distribution_algebra', 'distribution_algebra.examples', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0',
 'matplotlib>=3.6.2,<4.0.0',
 'numpy>=1.24.0,<2.0.0',
 'pydantic>=1.10.4,<2.0.0',
 'scipy>=1.9.3,<2.0.0',
 'wheel>=0.38.1']

setup_kwargs = {
    'name': 'distribution-algebra',
    'version': '0.1.9',
    'description': 'A python package that implements an easy-to-use interface for random variables, statistical distributions, and their algebra.',
    'long_description': '# distribution-algebra\nA python package that implements an easy-to-use interface for random\nvariables, statistical distributions, and their algebra.\n\nThis Python package is brought to you by [Vaibhav Karve](https://vaibhavkarve.github.io).\n\n`distribution-algebra` recognizes Normal, Lognormal, Beta and Poisson\ndistributions. The package implements an interface to easily construct\nuser-defined Univariate distributions as well Vectorized distributions.\n\nAdditional features include:\n- A `plot` function for probability density/mass function plotting.\n- A `draw` function for drawing random samples of specified size from a given distribution.\n- Addition and multiplication operations defined directly on distributions:\n  - For example, the sum of two Normal (Poisson) distributions is Normal (Poisson).\n  - The product of two Lognormal distributions is Lognormal.\n  - The sum of two arbitrary univariate distributions is expressed as a Vectorized distribution.\n\n\n![Example plot](https://github.com/vaibhavkarve/distribution-algebra/raw/main/docs/example_plot_univariate.png)\n\n\nThis package is written in Python v3.10, and is publicly available\nunder the [GNU-GPL-v3.0\nlicense](https://github.com/vaibhavkarve/normal-form/blob/main/LICENSE).\n\n\n# Installation and usage\n\nTo get started on using this package,\n\n1.  Istall Python 3.10 or higher.\n2.  `python3.10 -m pip install distribution-algebra`\n3.  Use it in a python script (or interactive REPL)\n\n    ```python\n    from distribution_algebra import Beta, Lognormal, Normal, Poisson\n\n    x: Normal = Normal(mean=1.0, var=9.0)\n\ty: Normal = Normal(mean=1.0, var=16.0)\n\n\tassert x + y == Normal(mean=2.0, var=25.0)\n    ```\n',
    'author': 'Vaibhav Karve',
    'author_email': 'vkarve@protonmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://vaibhavkarve.github.io/distribution-algebra/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
