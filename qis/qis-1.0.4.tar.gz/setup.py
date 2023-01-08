# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qis',
 'qis.data',
 'qis.examples',
 'qis.models',
 'qis.models.linear',
 'qis.models.ml',
 'qis.models.stats',
 'qis.perfstats',
 'qis.plots',
 'qis.plots.derived',
 'qis.portfolio',
 'qis.portfolio.optimization',
 'qis.portfolio.reports',
 'qis.portfolio.strats',
 'qis.utils']

package_data = \
{'': ['*'], 'qis': ['resources/*', 'resources/xml/*']}

install_requires = \
['matplotlib>=3.5.2',
 'numba>=0.55',
 'numpy>=1.22.4',
 'pandas>=0.19',
 'scipy>=1.3',
 'seaborn>=0.11.2',
 'statsmodels>=0.13.0']

setup_kwargs = {
    'name': 'qis',
    'version': '1.0.4',
    'description': 'Implementation of visualisation and reporting analytics for Quantitative Investment Strategies',
    'long_description': '# READ ME\n\nQIS stands for Quantitative investment strategies. The package implements analytics for analysis,\nsimulation, and visualization of quantitative strategies \n\n## **Installation**\n\n```python \npip install qis\n```\n\n## **Analytics**\n\nThe QIS package is split into subpackages based on the scope level.\n\nThe inclusion level is from a low dependency to higher dependency subpackages:\n\n\n1. utils is low level utilities for pandas and numpy operations\n\n2. perfstats is subpackage for performance statistics related to returns, volatilities, etc.\n\n3. plots is subpackage for plotting apis\n\n4. models includes several modules for analytical models split by applications\n\n5. portfolio is a high level package for analysis, simulation, and reporting of quant strategies\n\n6. data is a stand-alone package for data fetching using external apis\n\n7. example is modul with examples of QIS analytics\n\n\n',
    'author': 'Artur Sepp',
    'author_email': 'artursepp@gmail.com',
    'maintainer': 'Artur Sepp',
    'maintainer_email': 'artursepp@gmail.com',
    'url': 'https://github.com/ArturSepp/QuantInvestStrats',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
