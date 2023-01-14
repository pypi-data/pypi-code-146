# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clscurves', 'clscurves.plotter', 'clscurves.tests']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.4.2,<4.0.0',
 'numpy>=1.20.3,<2.0.0',
 'pandas>=1.2.4,<2.0.0',
 'scipy>=1.6.3,<2.0.0']

setup_kwargs = {
    'name': 'clscurves',
    'version': '0.1.0',
    'description': 'Compute and plot bootstrapped performance curves for classification problems.',
    'long_description': '# classification-curves\n\nA library for computing and plotting bootstrapped metrics (ROC curves,\nPrecision-Recall curves, etc.) to evaluate the performance of a classification\nmodel.\n\n## Example\n```python\nmg = MetricsGenerator(\n    predictions_df,\n    label_column = "label",\n    score_column = "score",\n    weight_column = "weight",\n    score_is_probability = False,\n    reverse_thresh = False,\n    num_bootstrap_samples = 20)\n\nmg.plot_pr(bootstrapped = True)\nmg.plot_roc()\n```\n        ',
    'author': 'Christopher Bryant',
    'author_email': 'cbryant@berkeley.edu',
    'maintainer': 'Christopher Bryant',
    'maintainer_email': 'cbryant@berkeley.edu',
    'url': 'https://github.com/chrismbryant/classification-curves',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
