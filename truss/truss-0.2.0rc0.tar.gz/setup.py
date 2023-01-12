# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['truss',
 'truss.contexts',
 'truss.contexts.image_builder',
 'truss.contexts.local_loader',
 'truss.environment_inference',
 'truss.local',
 'truss.model_frameworks',
 'truss.patch',
 'truss.templates',
 'truss.templates.control.control',
 'truss.templates.control.control.helpers',
 'truss.templates.custom.model',
 'truss.templates.custom.train',
 'truss.templates.huggingface_transformer.model',
 'truss.templates.keras.model',
 'truss.templates.lightgbm.model',
 'truss.templates.mlflow.model',
 'truss.templates.pipeline.model',
 'truss.templates.pytorch.model',
 'truss.templates.server',
 'truss.templates.server.common',
 'truss.templates.shared',
 'truss.templates.sklearn.model',
 'truss.templates.training',
 'truss.templates.xgboost.model',
 'truss.test_data.models.slow_load.model',
 'truss.test_data.patch_ping_test_server',
 'truss.test_data.truss_container_fs.app',
 'truss.test_data.truss_container_fs.app.common',
 'truss.test_data.truss_container_fs.app.model',
 'truss.test_data.truss_container_fs.app.shared',
 'truss.tests',
 'truss.tests.contexts.local_loader',
 'truss.tests.environments_inference',
 'truss.tests.local',
 'truss.tests.model_frameworks',
 'truss.tests.patch',
 'truss.tests.templates.control.control',
 'truss.tests.templates.control.control.helpers',
 'truss.tests.templates.core.server',
 'truss.tests.templates.core.server.common']

package_data = \
{'': ['*'],
 'truss': ['test_data/*', 'test_data/models/slow_load/*'],
 'truss.templates': ['control/*',
                     'custom/*',
                     'docs/*',
                     'huggingface_transformer/*',
                     'keras/*',
                     'lightgbm/*',
                     'mlflow/*',
                     'pipeline/*',
                     'pytorch/*',
                     'sklearn/*',
                     'xgboost/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'PyYAML>=6.0,<7.0',
 'cloudpickle>=2.2.0,<3.0.0',
 'msgpack-numpy>=0.4.7.1',
 'msgpack>=1.0.2',
 'numpy>=1.18',
 'packaging>=20.9,<21.0',
 'python-json-logger>=2.0.2',
 'python-on-whales>=0.46.0,<0.47.0',
 'single-source>=0.3.0,<0.4.0',
 'tenacity>=8.0.1,<9.0.0']

entry_points = \
{'console_scripts': ['truss = truss.cli:cli_group']}

setup_kwargs = {
    'name': 'truss',
    'version': '0.2.0rc0',
    'description': 'A seamless bridge from model development to model delivery',
    'long_description': '# Truss\n\n**Serve any model without boilerplate code**\n\n![Truss logo](https://raw.githubusercontent.com/basetenlabs/truss/main/docs/assets/truss_logo_horizontal.png)\n\n[![PyPI version](https://badge.fury.io/py/truss.svg)](https://badge.fury.io/py/truss)\n[![ci_status](https://github.com/basetenlabs/truss/actions/workflows/main.yml/badge.svg)](https://github.com/basetenlabs/truss/actions/workflows/main.yml)\n\nMeet Truss, a seamless bridge from model development to model delivery. Truss presents an open-source standard for packaging models built in any framework for sharing and deployment in any environment, local or production.\n\nGet started with the [end-to-end tutorial](https://truss.baseten.co/e2e).\n\n## What can I do with Truss?\n\nIf you\'ve ever tried to get a model out of a Jupyter notebook, Truss is for you.\n\nTruss exposes just the right amount of complexity around things like Docker and APIs without you really having to think about them. Here are some of the things Truss does:\n\n* 🏎 Turns your Python model into a microservice with a production-ready API endpoint, no need for Flask or Django.\n* 🎚 For most popular frameworks, includes automatic model serialization and deserialization.\n* 🛍 Freezes dependencies via Docker to make your training environment portable.\n* 🕰 Enables rapid iteration with local development that matches your production environment.\n* 🗃 Encourages shipping parsing and even business logic alongside your model with integrated pre- and post-processing functions.\n* 🤖 Supports running predictions on GPUs. (Currently limited to certain hardware, more coming soon)\n* 🙉 Bundles secret management to securely give your model access to API keys.\n\n## Installation\n\nTruss requires Python >=3.7, <3.11\n\nTo install from [PyPi](https://pypi.org/project/truss/), run:\n\n```\npip install truss\n```\n\nTo download the source code directly (for development), clone this repository and follow the setup commands in our [contributors\' guide](CONTRIBUTING.md).\n\nTruss is actively developed, and we recommend using the latest version. To update your Truss installation, run:\n\n```\npip install --upgrade truss\n```\n\nThough Truss is in beta, we do care about backward compatibility. Review the [release notes](docs/CHANGELOG.md) before upgrading, and note that we follow semantic versioning, so any breaking changes require the release of a new major version.\n\n## How to use Truss\n\nGenerate and serve predictions from a Truss with [this Jupyter notebook](docs/notebooks/sklearn_example.ipynb).\n\n### Quickstart: making a Truss\n\n```python\n!pip install --upgrade scikit-learn truss\n\nimport truss\nfrom sklearn.ensemble import RandomForestClassifier\nfrom sklearn.datasets import load_iris\n\n# Load the iris data set\niris = load_iris()\ndata_x = iris[\'data\']\ndata_y = iris[\'target\']\n\n# Train the model\nrfc = RandomForestClassifier()\nrfc.fit(data_x, data_y)\n\n# Create the Truss (serializing & packaging model)\ntr = truss.create(rfc, target_directory="iris_rfc_truss")\n\n# Serve a prediction from the model\ntr.predict({"inputs": [[0, 0, 0, 0]]})\n```\n\n### Package your model\n\nThe `truss.create()` command can be used with any supported framework:\n\n* [Hugging Face](https://truss.baseten.co/create/huggingface)\n* [LightGBM](https://truss.baseten.co/create/lightgbm)\n* [PyTorch](https://truss.baseten.co/create/pytorch)\n* [scikit-learn](https://truss.baseten.co/create/sklearn)\n* [Tensorflow](https://truss.baseten.co/create/tensorflow)\n* [XGBoost](https://truss.baseten.co/create/xgboost)\n\nBut in more complex cases, you can build a Truss manually for any model. Start with `truss init my_truss` and follow [this guide](https://truss.baseten.co/create/manual).\n\n### Serve your model locally\n\nServing your model with Truss, on Docker, lets you interface with your model via HTTP requests. Start your model server with:\n\n```\ntruss run-image iris_rfc_truss\n```\n\nThen, as long as the container is running, you can invoke the model as an API as follows:\n\n```\ncurl -X POST http://127.0.0.1:8080/v1/models/model:predict -d \'{"inputs": [[0, 0, 0, 0]]}\'\n```\n\n### Configure your model for deployment\n\nTruss is configurable to its core. Every Truss must include a file `config.yaml` in its root directory, which is automatically generated when the Truss is created. However, configuration is optional. Every configurable value has a sensible default, and a completely empty config file is valid.\n\nThe Truss we generated above in the quickstart sample has a good example of a typical Truss config:\n\n```yaml\nmodel_framework: sklearn\nmodel_metadata:\n  model_binary_dir: model\n  supports_predict_proba: true\npython_version: py39\nrequirements:\n- scikit-learn==1.0.2\n- threadpoolctl==3.0.0\n- joblib==1.1.0\n- numpy==1.20.3\n- scipy==1.7.3\n```\n\nFollow the [configuration guide](https://truss.baseten.co/develop/configuration) and use the complete reference of configurable properties to make your Truss perform exactly as you wish.\n\n### Deploy your model\n\nYou can deploy a Truss anywhere that can run a Docker image, as well as purpose-built platforms like [Baseten](https://baseten.co).\n\nFollow step-by-step deployment guides for the following platforms:\n\n* [AWS ECS](https://truss.baseten.co/deploy/aws)\n* [Baseten](https://truss.baseten.co/deploy/baseten)\n* [GCP Cloud Run](https://truss.baseten.co/deploy/gcp)\n\n## Contributing\n\nWe hope this vision excites you, and we gratefully welcome contributions in accordance with our [contributors\' guide](CONTRIBUTING.md) and [code of conduct](CODE_OF_CONDUCT.md).\n\nTruss was first developed at [Baseten](https://baseten.co) by maintainers Phil Howes, Pankaj Gupta, and Alex Gillmor.\n\n## GitHub Codespace\n\nIf your organization allows to access to GitHub Codespaces, you can launch a Codespace for truss development. If you are a GPU Codespace, make sure to use the `.devcontainer/gpu/devcontainer.json` configuration to have access to a GPU and be able to use it in Docker with truss.\n',
    'author': 'Pankaj Gupta',
    'author_email': 'pankaj@baseten.co',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/basetenlabs/truss',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
