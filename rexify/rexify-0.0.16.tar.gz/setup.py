# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rexify',
 'rexify.features',
 'rexify.features.transform',
 'rexify.models',
 'rexify.models.callbacks',
 'rexify.models.ranking',
 'rexify.models.retrieval']

package_data = \
{'': ['*']}

install_requires = \
['kfp>=1.8.0,<2.0.0',
 'numpy>=1.20.3',
 'pandas>=1.4.0,<2.0.0',
 'scikit-learn>=1.0.0,<2.0.0',
 'tensorflow_recommenders>=0.7.2']

extras_require = \
{':sys_platform != "darwin"': ['tensorflow>=2.6.0,<3.0.0',
                               'scann>=1.2.0,<2.0.0'],
 ':sys_platform == "darwin"': ['tensorflow_metal>=0.5.0,<0.6.0',
                               'tensorflow_macos>=2.6.0,<3.0.0']}

setup_kwargs = {
    'name': 'rexify',
    'version': '0.0.16',
    'description': 'Streamlined Recommender System workflows with TensorFlow and Kubeflow',
    'long_description': '<p align="center">\n    <br>\n    <img src="https://storage.googleapis.com/rexify/1659986918545.png" height="200"/>\n    <br>\n<p>\n\n<p align="center">\n    <a href="https://circleci.com/gh/joseprsm/rexify">\n        <img alt="Build" src="https://img.shields.io/circleci/build/github/joseprsm/rexify?style=flat-square">\n    </a>\n    <a href="https://github.com/joseprsm/rexify/blob/main/LICENSE">\n        <img alt="License" src="https://img.shields.io/github/license/joseprsm/rexify?style=flat-square">\n    </a>\n    <a href="https://rexify.readthedocs.io">\n        <img alt="Documentation" src="https://img.shields.io/badge/documentation-online-success?style=flat-square">\n    </a>\n    <a href="https://pypi.org/project/rexify/">\n        <img alt="GitHub release" src="https://img.shields.io/github/v/release/joseprsm/rexify?style=flat-square">\n    </a>\n</p>\n\nRexify is a library to streamline recommender systems model development.\n\nIn essence, Rexify adapts dynamically to your data, and outputs high-performing TensorFlow\nmodels that may be used wherever you want, independently of your data. Rexify also includes\nmodules to deal with feature engineering as Scikit-Learn Transformers and Pipelines.\n\nWith Rexify, users may easily train Recommender Systems models, just by specifying what their\ndata looks like. Rexify also comes equipped with pre-built machine learning pipelines which can\nbe used serverlessly. \n\n## What is Rexify?\n\nRexify is a low-code personalization tool, that makes use of traditional machine learning \nframeworks, such as Scikit-Learn and TensorFlow, to create scalable Recommender Systems\nworkflows that anyone can use.\n\n### Who is it for?\n\nRexify is a project that simplifies and standardizes the workflow of recommender systems. It is \nmostly geared towards people with little to no machine learning knowledge, that want to implement\nsomewhat scalable Recommender Systems in their applications.\n\n## Installation\n\nThe easiest way to install Rexify is via `pip`:\n\n```shell\npip install rexify\n```\n\n## Quick Tour\n\nRexify is meant to be usable right out of the box. All you need to set up your model is interaction\ndata - something that kind of looks like this:\n\n| user_id | item_id | timestamp  | event_type  |\n|---------|---------|------------|-------------|\n| 22      | 67      | 2021/05/13 | Purchase    |\n| 37      | 9       | 2021/04/11 | Page View   |\n| 22      | 473     | 2021/04/11 | Add to Cart |\n| ...     | ...     | ...        | ...         |\n| 358     | 51      | 2021/04/11 | Purchase    |\n\nAdditionally, we\'ll have to have configured a schema for the data.\nThis schema is what will allow Rexify to generate a dynamic model and preprocessing steps.\nThe schema should be comprised of two dictionaries (`user`, `ìtem`) and two key-value \npairs: `event_type` (which should point to the column of the event type) and `timestamp` (\nwhich should point to the timestamp column)\n\nEach of these dictionaries should consist of features and internal data types, \nsuch as: `id`, `category`, `number`. More data types will be available \nin the future.\n\n```json\n{\n  "user": {\n    "user_id": "id",\n    "age": "number"\n  },\n  "item": {\n    "item_id": "id",\n    "category": "category"\n  },\n  "timestamp": "timestamp"\n  "event_type": "event_type"\n}\n```\n\nEssentially, what Rexify will do is take the schema, and dynamically adapt to the data.\n\nThere are two main components in Rexify workflows: `FeatureExtractor` and `Recommender`.\n\nThe `FeatureExtractor` is a scikit-learn Transformer that basically takes the schema of \nthe data, and transforms the event data accordingly. Another method `.make_dataset()`, \nconverts the transformed data into a `tf.data.Dataset`, all correctly configured to be fed\nto the `Recommender` model.\n\n`Recommender` is a `tfrs.Model` that basically implements the Query and Candidate towers. \nDuring training, the Query tower will take the user ID, user features, and context, to \nlearn an embedding; the Candidate tower will do the same for the item ID and its features. \n\nMore information about how the `FeatureExtractor` and the `Recommender` works can be found \n[here](https://rexify.readthedocs.io/en/latest/overview/architecture.html). \n\nA sample Rexify workflow should sort of look like this:\n\n````python\n\nimport pandas as pd\n\nfrom rexify import Schema, FeatureExtractor, Recommender\n\nevents = pd.read_csv(\'path/to/events/data\')\n\nschema = Schema.load(\'path/to/schema\')\n\nfeat = FeatureExtractor(schema, users=\'path/to/users/data\', items=\'path/to/events/data\')\nx = feat.fit_transform(events)\nx = feat.make_dataset(x)\n\nmodel = Recommender(**feat.model_params)\nmodel.compile()\nmodel.fit(events, batch_size=512)\n````\n\nWhen training is complete, you\'ll have a trained `tf.keras.Model` ready to be used, as\nyou normally would. \n\n## License\n\n[MIT](https://github.com/joseprsm/rexify/blob/main/LICENSE)\n',
    'author': 'José Medeiros',
    'author_email': 'joseprsm@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
