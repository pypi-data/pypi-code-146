# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['numalogic',
 'numalogic.models',
 'numalogic.models.autoencoder',
 'numalogic.models.autoencoder.variants',
 'numalogic.models.forecast',
 'numalogic.models.forecast.variants',
 'numalogic.models.threshold',
 'numalogic.preprocess',
 'numalogic.registry',
 'numalogic.synthetic',
 'numalogic.tools']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.23,<2.0',
 'pandas>=1.4,<2.0',
 'protobuf>=3.20,<3.21',
 'scikit-learn>=1.0,<2.0']

extras_require = \
{'mlflow': ['mlflow-skinny>=2.0.1,<2.1.0']}

setup_kwargs = {
    'name': 'numalogic',
    'version': '0.3.1',
    'description': 'Collection of operational Machine Learning models and tools.',
    'long_description': "# numalogic\n\n[![Build](https://github.com/numaproj/numalogic/actions/workflows/ci.yml/badge.svg)](https://github.com/numaproj/numalogic/actions/workflows/ci.yml)\n[![codecov](https://codecov.io/gh/numaproj/numalogic/branch/main/graph/badge.svg?token=020HF97A32)](https://codecov.io/gh/numaproj/numalogic)\n[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)\n[![slack](https://img.shields.io/badge/slack-numaproj-brightgreen.svg?logo=slack)](https://join.slack.com/t/numaproj/shared_invite/zt-19svuv47m-YKHhsQ~~KK9mBv1E7pNzfg)\n[![Release Version](https://img.shields.io/github/v/release/numaproj/numalogic?label=numalogic)](https://github.com/numaproj/numalogic/releases/latest)\n\n\n## Background\nNumalogic is a collection of ML models and algorithms for operation data analytics and AIOps. \nAt Intuit, we use Numalogic at scale for continuous real-time data enrichment including \nanomaly scoring. We assign an anomaly score (ML inference) to any time-series \ndatum/event/message we receive on our streaming platform (say, Kafka). 95% of our \ndata sets are time-series, and we have a complex flowchart to execute ML inference on \nour high throughput sources. We run multiple models on the same datum, say a model that is \nsensitive towards +ve sentiments, another more tuned towards -ve sentiments, and another \noptimized for neutral sentiments. We also have a couple of ML models trained for the same \ndata source to provide more accurate scores based on the data density in our model store. \nAn ensemble of models is required because some composite keys in the data tend to be less \ndense than others, e.g., forgot-password interaction is less frequent than a status check \ninteraction. At runtime, for each datum that arrives, models are picked based on a conditional \nforwarding filter set on the data density. ML engineers need to worry about only their \ninference container; they do not have to worry about data movement and quality assurance.\n\n## Numalogic realtime training \nFor an always-on ML platform, the key requirement is the ability to train or retrain models \nautomatically based on the incoming messages. The composite key built at per message runtime \nlooks for a matching model, and if the model turns out to be stale or missing, an automatic \nretriggering is applied. The conditional forwarding feature of the platform improves the \ndevelopment velocity of the ML developer when they have to make a decision whether to forward \nthe result further or drop it after a trigger request.\n\n\n## Key Features\n\n1. Ease of use: simple and efficient tools for predictive data analytics\n2. Reusability: all the functionalities can be re-used in various contexts\n3. Model selection: easy to compare, validate, fine-tune and choose the model that works best with each data set\n4. Data processing: readily available feature extraction, scaling, transforming and normalization tools\n5. Extensibility: adding your own functions or extending over the existing capabilities\n6. Model Storage: out-of-the-box support for MLFlow and support for other model ML lifecycle management tools\n\n## Use Cases\n1. Deployment failure detection\n2. System failure detection for node failures or crashes\n3. Fraud detection\n4. Network intrusion detection\n5. Forecasting on time series data\n\n## Getting Started\n\nFor set-up information and running your first pipeline using numalogic, please see our [getting started guide](./quick-start.md).\n\n\n## Installation\n\nNumalogic requires Python 3.8 or higher.\n\n### Prerequisites\nNumalogic needs [PyTorch](https://pytorch.org/) and \n[PyTorch Lightning](https://pytorch-lightning.readthedocs.io/en/stable/) to work. \nBut since these packages are platform dependendent, \nthey are not included in the numalogic package itself. Kindly install them first.\n\nNumalogic supports the following pytorch versions:\n- 1.11.x\n- 1.12.x\n- 1.13.x\n\nOther versions do work, it is just that they are not tested.\n\nnumalogic can be installed using pip.\n```shell\npip install numalogic\n```\n\nIf using mlflow for model registry, install using:\n```shell\npip install numalogic[mlflow]\n```\n\n### Build locally\n\n1. Install [Poetry](https://python-poetry.org/docs/):\n    ```\n    curl -sSL https://install.python-poetry.org | python3 -\n    ```\n2. To activate virtual env:\n    ```\n    poetry shell\n    ```\n3. To install dependencies:\n    ```\n    poetry install --with dev,torch\n    ```\n   If extra dependencies are needed:\n    ```\n    poetry install --all-extras\n    ```\n4. To run unit tests:\n    ```\n    make test\n    ```\n5. To format code style using black:\n    ```\n    make lint\n    ```\n\n## Contributing\nWe would love contributions in the numalogic project in one of the following (but not limited to) areas:\n\n- Adding new time series anomaly detection models\n- Making it easier to add user's custom models\n- Support for additional model registry frameworks\n\nFor contribution guildelines please refer [here](https://github.com/numaproj/numaproj/blob/main/CONTRIBUTING.md).\n\n\n## Resources\n- [QUICK_START](docs/quick-start.md)\n- [EXAMPLES](examples)\n- [CONTRIBUTING](https://github.com/numaproj/numaproj/blob/main/CONTRIBUTING.md)\n",
    'author': 'Numalogic Developers',
    'author_email': 'None',
    'maintainer': 'Avik Basu',
    'maintainer_email': 'avikbasu93@gmail.com',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
