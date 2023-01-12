# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dbt',
 'dbt.adapters.fal',
 'dbt.adapters.fal_experimental',
 'dbt.adapters.fal_experimental.support',
 'dbt.adapters.fal_experimental.telemetry',
 'dbt.adapters.fal_experimental.teleport_support',
 'dbt.adapters.fal_experimental.utils',
 'dbt.fal.adapters.python',
 'dbt.fal.adapters.teleport',
 'dbt.include.fal',
 'dbt.include.fal_experimental']

package_data = \
{'': ['*'],
 'dbt.include.fal': ['macros/*', 'macros/materializations/*'],
 'dbt.include.fal_experimental': ['macros/materializations/*']}

install_requires = \
['backports.functools_lru_cache>=1.6.4,<2.0.0',
 'dbt-core>=1.3.0b1,<1.4',
 'isolate[grpc]>=0.7,<0.8',
 'pandas>=1.3.4,<2.0.0',
 'posthog>=1.4.5,<2.0.0',
 'sqlalchemy>=1.4.41,<2.0.0']

extras_require = \
{'bigquery': ['google-cloud-bigquery[pandas]>=2,<3'],
 'cloud': ['isolate-cloud>=0.6.11', 'dill>=0.3.5.1'],
 'redshift': ['sqlalchemy-redshift>=0.8.9,<0.9.0'],
 'snowflake': ['snowflake-connector-python[pandas]>=2.7.10,<2.8.0'],
 'teleport': ['s3fs>=2022.8.2'],
 'trino': ['trino[sqlalchemy]>=0.319.0,<0.320.0']}

setup_kwargs = {
    'name': 'dbt-fal',
    'version': '1.3.11',
    'description': 'Simplest way to run dbt python models.',
    'long_description': '# Welcome to dbt-fal 👋\n\ndbt-fal adapter is the ✨easiest✨ way to run your [dbt Python models](https://docs.getdbt.com/docs/building-a-dbt-project/building-models/python-models).\n\nStarting with dbt v1.3, you can now build your dbt models in Python. This leads to some cool use cases that was once difficult to build with SQL alone. Some examples are:\n\n- Using Python stats libraries to calculate stats\n- Building forecasts\n- Building other predictive models such as classification and clustering\n\nThis is fantastic! BUT, there is still one issue though! The developer experience with Snowflake and Bigquery is not great, and there is no Python support for Redshift and Postgres.\n\ndbt-fal provides the best environment to run your Python models that works with all other data warehouses! With dbt-fal, you can:\n\n- Build and test your models locally\n- Isolate each model to run in its own environment with its own dependencies\n- [Coming Soon] Run your Python models in the ☁️ cloud ☁️ with elasticly scaling Python environments.\n- [Coming Soon] Even add GPUs to your models for some heavier workloads such as training ML models.\n\n## Getting Started\n\n### 1. Install dbt-fal\n`pip install dbt-fal[bigquery, snowflake]` *Add your current warehouse here*\n\n### 2. Update your `profiles.yml` and add the fal adapter\n\n```yaml\njaffle_shop:\n  target: dev_with_fal\n  outputs:\n    dev_with_fal:\n      type: fal\n      db_profile: dev_bigquery # This points to your main adapter\n    dev_bigquery:\n      type: bigquery\n      ...\n```\n\nDon\'t forget to point to your main adapter with the `db_profile` attribute. This is how the fal adapter knows how to connect to your data warehouse.\n\n### 3. `dbt run`!\nThat is it! It is really that simple 😊\n\n### 4. [🚨 Cool Feature Alert 🚨] Environment management with dbt-fal\nIf you want some help with environment management (vs sticking to the default env that the dbt process runs in), you can create a fal_project.yml in the same folder as your dbt project and have “named environments”:\n\nIn your dbt project folder:\n```bash\n$ touch fal_project.yml\n\n# Paste the config below\nenvironments:\n  - name: ml\n    type: venv\n    requirements:\n      - prophet\n```\n\nand then in your dbt model:\n\n```bash\n$ vi models/orders_forecast.py\n\ndef model(dbt, fal):\n    dbt.config(fal_environment="ml") # Add this line\n\n    df: pd.DataFrame = dbt.ref("orders_daily")\n```\n\nThe `dbt.config(fal_environment=“ml”)` will give you an isolated clean env to run things in, so you dont pollute your package space.\n\n### 5. [Coming Soon™️] Move your compute to the Cloud!\nLet us know if you are interested in this. We are looking for beta users.\n',
    'author': 'Features & Labels',
    'author_email': 'hello@fal.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fal-ai/fal/adapter',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.2,<3.12',
}


setup(**setup_kwargs)
