# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['scandeval']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'datasets>=2.7.0,<3.0.0',
 'evaluate>=0.3.0,<1.0.0',
 'flax>=0.6.3,<1.0.0',
 'huggingface-hub>=0.7.0,<1.0.0',
 'jax>=0.4.1,<1.0.0',
 'jaxlib>=0.4.1,<1.0.0',
 'numpy>=1.23.0,<2.0.0',
 'pandas>=1.4.0,<2.0.0',
 'protobuf>=3.20.0,<3.21.0',
 'pyinfer>=0.0.3,<1.0.0',
 'python-dotenv>=0.20.0,<1.0.0',
 'sacremoses>=0.0.53,<1.0.0',
 'sentencepiece>=0.1.96,<1.0.0',
 'seqeval>=1.2.2,<2.0.0',
 'termcolor>=1.1.0,<2.0.0',
 'torch>=1.12.1,<2.0.0',
 'tqdm>=4.62.0,<5.0.0',
 'transformers>=4.20.0,<5.0.0']

entry_points = \
{'console_scripts': ['scandeval = scandeval.cli:benchmark']}

setup_kwargs = {
    'name': 'scandeval',
    'version': '6.2.0',
    'description': 'Evaluation of pretrained language models on mono- or multilingual Scandinavian language tasks.',
    'long_description': '<div align=\'center\'>\n<img src="https://raw.githubusercontent.com/saattrupdan/ScandEval/main/gfx/scandeval.png" width="517" height="217">\n</div>\n\n### Evaluation of pretrained language models on mono- or multilingual Scandinavian language tasks.\n\n______________________________________________________________________\n[![PyPI Status](https://badge.fury.io/py/scandeval.svg)](https://pypi.org/project/scandeval/)\n[![Documentation](https://img.shields.io/badge/docs-passing-green)](https://saattrupdan.github.io/ScandEval/scandeval.html)\n[![License](https://img.shields.io/github/license/saattrupdan/ScandEval)](https://github.com/saattrupdan/ScandEval/blob/main/LICENSE)\n[![LastCommit](https://img.shields.io/github/last-commit/saattrupdan/ScandEval)](https://github.com/saattrupdan/ScandEval/commits/main)\n[![Code Coverage](https://img.shields.io/badge/Coverage-74%25-yellow.svg)](https://github.com/saattrupdan/ScandEval/tree/main/tests)\n[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.0-4baaaa.svg)](https://github.com/saattrupdan/ScandEval/blob/main/CODE_OF_CONDUCT.md)\n\n\n## Installation\nTo install the package simply write the following command in your favorite terminal:\n```\n$ pip install scandeval\n```\n\n## Quickstart\n### Benchmarking from the Command Line\nThe easiest way to benchmark pretrained models is via the command line interface. After\nhaving installed the package, you can benchmark your favorite model like so:\n```\n$ scandeval --model-id <model-id>\n```\n\nHere `model_id` is the HuggingFace model ID, which can be found on the [HuggingFace\nHub](https://huggingface.co/models). By default this will benchmark the model on all\nthe datasets eligible. If you want to benchmark on a specific dataset, this can be done\nvia the `--dataset` flag. This will for instance evaluate the model on the\n`AngryTweets` dataset:\n```\n$ scandeval --model-id <model-id> --dataset angry-tweets\n```\n\nWe can also separate by language. To benchmark all Danish models on all Danish\ndatasets, say, this can be done using the `language` tag, like so:\n```\n$ scandeval --language da\n```\n\nMultiple models, datasets and/or languages can be specified by just attaching multiple\narguments. Here is an example with two models:\n```\n$ scandeval --model-id <model-id1> --model-id <model-id2> --dataset angry-tweets\n```\n\nThe specific model version to use can also be added after the suffix \'@\':\n```\n$ scandeval --model-id <model-id>@<commit>\n```\n\nIt can be a branch name, a tag name, or a commit id. It defaults to \'main\' for latest.\n\nSee all the arguments and options available for the `scandeval` command by typing\n```\n$ scandeval --help\n```\n\n### Benchmarking from a Script\nIn a script, the syntax is similar to the command line interface. You simply initialise\nan object of the `Benchmarker` class, and call this benchmark object with your favorite\nmodels and/or datasets:\n```\n>>> from scandeval import Benchmarker\n>>> benchmark = Benchmarker()\n>>> benchmark(\'<model-id>\')\n```\n\nTo benchmark on a specific dataset, you simply specify the second argument, shown here\nwith the `AngryTweets` dataset again:\n```\n>>> benchmark(\'<model_id>\', \'angry-tweets\')\n```\n\nIf you want to benchmark a subset of all the models on the Hugging Face Hub, you can\nspecify several parameters in the `Benchmarker` initializer to narrow down the list of\nmodels to the ones you care about. As a simple example, the following would benchmark\nall the Nynorsk models on Nynorsk datasets:\n```\n>>> benchmark = Benchmarker(language=\'nn\')\n>>> benchmark()\n```\n\n\n## Documentation\n\nSee the full documentation [here](https://saattrupdan.github.io/ScandEval/scandeval.html).\n\n\n## Citing ScandEval\nIf you want to cite the framework then feel free to use this:\n```\n@article{nielsen2022scandeval,\n  title={ScandEval: Evaluation of language models on mono- or multilingual Scandinavian language tasks.},\n  author={Nielsen, Dan Saattrup},\n  journal={GitHub. Note: https://github.com/saattrupdan/ScandEval},\n  year={2022}\n}\n```\n\n## Remarks\nThe image used in the logo has been created by the amazing [Scandinavia and the\nWorld](https://satwcomic.com/) team. Go check them out!\n\n\n## Project structure\n```\n.\n├── .flake8\n├── .github\n│\xa0\xa0 └── workflows\n│\xa0\xa0     ├── ci.yaml\n│\xa0\xa0     └── docs.yaml\n├── .gitignore\n├── .pre-commit-config.yaml\n├── CHANGELOG.md\n├── LICENSE\n├── README.md\n├── gfx\n│\xa0\xa0 └── scandeval.png\n├── makefile\n├── notebooks\n├── poetry.toml\n├── pyproject.toml\n├── src\n│\xa0\xa0 ├── scandeval\n│\xa0\xa0 │\xa0\xa0 ├── __init__.py\n│\xa0\xa0 │\xa0\xa0 ├── benchmark_config_factory.py\n│\xa0\xa0 │\xa0\xa0 ├── benchmark_dataset.py\n│\xa0\xa0 │\xa0\xa0 ├── benchmarker.py\n│\xa0\xa0 │\xa0\xa0 ├── callbacks.py\n│\xa0\xa0 │\xa0\xa0 ├── cli.py\n│\xa0\xa0 │\xa0\xa0 ├── config.py\n│\xa0\xa0 │\xa0\xa0 ├── dataset_configs.py\n│\xa0\xa0 │\xa0\xa0 ├── dataset_factory.py\n│\xa0\xa0 │\xa0\xa0 ├── dataset_tasks.py\n│\xa0\xa0 │\xa0\xa0 ├── exceptions.py\n│\xa0\xa0 │\xa0\xa0 ├── hf_hub.py\n│\xa0\xa0 │\xa0\xa0 ├── languages.py\n│\xa0\xa0 │\xa0\xa0 ├── model_loading.py\n│\xa0\xa0 │\xa0\xa0 ├── named_entity_recognition.py\n│\xa0\xa0 │\xa0\xa0 ├── question_answering.py\n│\xa0\xa0 │\xa0\xa0 ├── question_answering_trainer.py\n│\xa0\xa0 │\xa0\xa0 ├── scores.py\n│\xa0\xa0 │\xa0\xa0 ├── sequence_classification.py\n│\xa0\xa0 │\xa0\xa0 ├── speed_benchmark.py\n│\xa0\xa0 │\xa0\xa0 ├── types.py\n│\xa0\xa0 │\xa0\xa0 └── utils.py\n│\xa0\xa0 └── scripts\n│\xa0\xa0     ├── create_angry_tweets.py\n│\xa0\xa0     ├── create_dane.py\n│\xa0\xa0     ├── create_mim_gold_ner.py\n│\xa0\xa0     ├── create_norec.py\n│\xa0\xa0     ├── create_norne.py\n│\xa0\xa0     ├── create_scala.py\n│\xa0\xa0     ├── create_scandiqa.py\n│\xa0\xa0     ├── create_suc3.py\n│\xa0\xa0     ├── create_swerec.py\n│\xa0\xa0     ├── create_wikiann_fo.py\n│\xa0\xa0     ├── fill_in_missing_model_metadata.py\n│\xa0\xa0     ├── fix_dot_env_file.py\n│\xa0\xa0     ├── load_ud_pos.py\n│\xa0\xa0     └── versioning.py\n└── tests\n    ├── __init__.py\n    ├── conftest.py\n    ├── test_benchmark_config_factory.py\n    ├── test_benchmark_dataset.py\n    ├── test_benchmarker.py\n    ├── test_callbacks.py\n    ├── test_cli.py\n    ├── test_config.py\n    ├── test_dataset_configs.py\n    ├── test_dataset_factory.py\n    ├── test_dataset_tasks.py\n    ├── test_exceptions.py\n    ├── test_hf_hub.py\n    ├── test_languages.py\n    ├── test_model_loading.py\n    ├── test_named_entity_recognition.py\n    ├── test_question_answering.py\n    ├── test_question_answering_trainer.py\n    ├── test_scores.py\n    ├── test_sequence_classification.py\n    ├── test_speed_benchmark.py\n    ├── test_types.py\n    └── test_utils.py\n```\n',
    'author': 'Dan Saattrup Nielsen',
    'author_email': 'saattrupdan@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://scandeval.github.io',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
