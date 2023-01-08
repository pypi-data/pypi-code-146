# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src', 'metahyper': 'src/metahyper'}

packages = \
['metahyper',
 'neps',
 'neps.optimizers',
 'neps.optimizers.bayesian_optimization',
 'neps.optimizers.bayesian_optimization.acquisition_functions',
 'neps.optimizers.bayesian_optimization.acquisition_samplers',
 'neps.optimizers.bayesian_optimization.kernels',
 'neps.optimizers.bayesian_optimization.kernels.grakel_replace',
 'neps.optimizers.bayesian_optimization.models',
 'neps.optimizers.grid_search',
 'neps.optimizers.multi_fidelity',
 'neps.optimizers.multi_fidelity_prior',
 'neps.optimizers.random_search',
 'neps.optimizers.regularized_evolution',
 'neps.plot',
 'neps.search_spaces',
 'neps.search_spaces.architecture',
 'neps.search_spaces.architecture.cfg_variants',
 'neps.search_spaces.hyperparameters',
 'neps.status',
 'neps.utils',
 'neps_examples',
 'neps_examples.basic_usage',
 'neps_examples.convenience',
 'neps_examples.efficiency',
 'neps_examples.experimental']

package_data = \
{'': ['*']}

install_requires = \
['ConfigSpace>=0.4.19,<0.5.0',
 'grakel>=0.1.9,<0.2.0',
 'matplotlib>=3.4,<4.0',
 'more-itertools>=9.0.0,<10.0.0',
 'networkx>=2.6.3,<3.0.0',
 'nltk>=3.6.4,<4.0.0',
 'pandas>=1.3.1,<2.0.0',
 'path>=16.2.0,<17.0.0',
 'portalocker>=2.6.0,<3.0.0',
 'scipy>=1.7,<2.0',
 'seaborn>=0.12.1,<0.13.0',
 'statsmodels>=0.13.2,<0.14.0',
 'termcolor>=1.1.0,<2.0.0',
 'torch>=1.7.0,<1.13.0']

extras_require = \
{':python_version < "3.8"': ['numpy>=1.21.0,<1.22.0'],
 ':python_version >= "3.8"': ['numpy>=1.22.0,<2.0.0']}

setup_kwargs = {
    'name': 'neural-pipeline-search',
    'version': '0.8.1',
    'description': 'Neural Pipeline Search helps deep learning experts find the best neural pipeline.',
    'long_description': '# Neural Pipeline Search (NePS)\n\n[![PyPI version](https://img.shields.io/pypi/v/neural-pipeline-search?color=informational)](https://pypi.org/project/neural-pipeline-search/)\n[![Python versions](https://img.shields.io/pypi/pyversions/neural-pipeline-search)](https://pypi.org/project/neural-pipeline-search/)\n[![License](https://img.shields.io/pypi/l/neural-pipeline-search?color=informational)](LICENSE)\n[![Tests](https://github.com/automl/neps/actions/workflows/tests.yaml/badge.svg)](https://github.com/automl/neps/actions)\n\nNePS helps deep learning experts to optimize the hyperparameters and/or architecture of their deep learning pipeline with:\n\n- Hyperparameter Optimization (HPO) ([example](neps_examples/basic_usage/hyperparameters.py))\n- Neural Architecture Search (NAS) ([example](neps_examples/basic_usage/architecture.py), [paper](https://openreview.net/forum?id=Ok58hMNXIQ))\n- Joint Architecture and Hyperparameter Search (JAHS) ([example](neps_examples/basic_usage/architecture_and_hyperparameters.py), [paper](https://openreview.net/forum?id=_HLcjaVlqJ))\n\nFor efficiency and convenience NePS allows you to\n\n- Add your intuition as priors for the search ([example HPO](neps_examples/expert_prior_for_hyperparameters), [example JAHS](neps_examples/expert_prior_for_hyperparameters), [paper](https://openreview.net/forum?id=MMAeCXIa89))\n- Utilize low fidelity (e.g., low epoch) evaluations to focus on promising configurations ([example](neps_examples/efficiency/parallelization.md), [paper](https://openreview.net/forum?id=ds21dwfBBH))\n- Trivially parallelize across machines ([example](neps_examples/efficiency/parallelization.md), [documentation](https://automl.github.io/neps/latest/parallelization/))\n\nOr [all of the above](neps_examples/efficiency/multi_fidelity_and_expert_priors.md) for maximum efficiency!\n\n## Note\n\nAs indicated with the `v0.x.x` version number, NePS is early stage code and APIs might change in the future.\n\n## Documentation\n\nPlease have a look at our [documentation](https://automl.github.io/neps/latest/) and [examples](neps_examples).\n\n## Installation\n\nUsing pip\n\n```bash\npip install neural-pipeline-search\n```\n\n## Usage\n\nUsing `neps` always follows the same pattern:\n\n1. Define a `run_pipeline` function that evaluates architectures/hyperparameters for your problem\n1. Define a search space `pipeline_space` of architectures/hyperparameters\n1. Call `neps.run` to optimize `run_pipeline` over `pipeline_space`\n\nIn code, the usage pattern can look like this:\n\n```python\nimport neps\nimport logging\n\n# 1. Define a function that accepts hyperparameters and computes the validation error\ndef run_pipeline(hyperparameter_a: float, hyperparameter_b: int):\n    validation_error = -hyperparameter_a * hyperparameter_b\n    return validation_error\n\n\n# 2. Define a search space of hyperparameters; use the same names as in run_pipeline\npipeline_space = dict(\n    hyperparameter_a=neps.FloatParameter(lower=0, upper=1),\n    hyperparameter_b=neps.IntegerParameter(lower=1, upper=100),\n)\n\n# 3. Call neps.run to optimize run_pipeline over pipeline_space\nlogging.basicConfig(level=logging.INFO)\nneps.run(\n    run_pipeline=run_pipeline,\n    pipeline_space=pipeline_space,\n    root_directory="usage_example",\n    max_evaluations_total=5,\n)\n```\n\nFor more details and features please have a look at our [documentation](https://automl.github.io/neps/latest/) and [examples](neps_examples).\n\n## Analysing runs\n\nSee our [documentation on analysing runs](https://automl.github.io/neps/latest/analyse).\n\n## Alternatives\n\nNePS does not cover your use-case? Have a look at [some alternatives](https://automl.github.io/neps/latest/alternatives).\n\n## Contributing\n\nPlease see the [documentation for contributors](https://automl.github.io/neps/latest/contributing/).\n',
    'author': 'Danny Stoll',
    'author_email': 'stolld@cs.uni-freiburg.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/automl/neps',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
