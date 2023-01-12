# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['botorchex', 'botorchex.acquisition', 'botorchex.acquisition.multi_objective']

package_data = \
{'': ['*']}

install_requires = \
['botorch>=0.8.1,<0.9.0']

setup_kwargs = {
    'name': 'botorchex',
    'version': '0.1.0',
    'description': '',
    'long_description': '# botorchex\n\nBotorch extention library including custom acquistion functions and surrogate models.\n\n## Installation \n\n```\n$ pip install botorchex\n```\n\n## Ease to use\n\nBotorch compatible interface.\n\n## Implementation List\n### Custom Acqusition function\n\n* Multi Objective Monte-Carlo Probability Improvement\nThis acquistion function can deacrease more computational resource(wall-time) comparing to other multi objective acqusition function. This performance especially is shown in the more than 3 objctive cases. However, the convergence speed is longer than the others and there is no theoretical background. \n\n```python\nfrom botorch.models.gp_regression import SingleTaskGP\nfrom botorch.models.model_list_gp_regression import ModelListGP\n\nfrom botorchex.acquisition.multi_objective.monte_carlo import qMultiProbabilityOfImprovement\n\nmodel1 = SingleTaskGP(train_X, train_Y[0, :])\nmodel2 = SingleTaskGP(train_X, train_Y[1, :])\n# we assume the outputs are independent each other.\nbest_f = train_Y.max(dim=1)\nmodes = ModelListGP([model1, model2])\nqPI = qMultiProbabilityOfImprovement(models, best_f)\nqmpi = qMPI(test_X)\n```\n\nIf you want to know more examples, you can check the example([multi_objective_bo.ipynb](https://github.com/0h-n0/botorchex/blob/main/tutorials/multi_objective_bo.ipynb))\n\n### Custom Surrogates\n\n* GNN based surrogates?\n\n### Referances\n\n* https://botorch.org/\n* https://gpytorch.ai/\n',
    'author': '0h-n0',
    'author_email': 'kbu94982@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
