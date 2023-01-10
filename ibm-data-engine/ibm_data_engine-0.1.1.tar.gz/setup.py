# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ibm_data_engine']

package_data = \
{'': ['*']}

install_requires = \
['feast>=0.25.0,<0.26.0', 'ibmcloudsql>=0.5.11,<0.6.0']

setup_kwargs = {
    'name': 'ibm-data-engine',
    'version': '0.1.1',
    'description': 'Feast offline feature store implementation backed by the IBM Cloud Data Engine',
    'long_description': '[Feast](https://feast.dev/) plugin for IBM Cloud.  \nThis plugin implements Feast\'s offline store backed using [IBM Cloud Data Engine](https://www.ibm.com/cloud/data-engine) and [IBM Cloud Object Storage](https://www.ibm.com/cloud/object-storage)\n\n# Installation\n\nProject dependencies can be installed in a dedicated virtual environment\nby running the following command:\n\n```bash\npoetry install\n```\n\n# Testing and Linting\n\n```bash\npoetry run pytest tests/\npoetry run pylint ibm_data_engine\n```\n\n# Test with Feast\n\nYou use it with [Feast](https://feast.dev/) by defining your offline store and data sources.\nThe instructions below illustrate how it can be used in\n[feast-ibm-quickstart](https://github.com/IBM/feast-ibm-quickstart).\n\n## Define dependency\n\nThis library is currently not published in [PyPI](https://pypi.org/); you will have to\npoint to the repository directly. The easiest way to do it is to clone\nthe repository, and define the dependency as a path in `feast-ibm-quickstart`.\n\n```toml\nibm-data-engine = { path = "/path/to/ibm-data-engine" }\n```\n\nAfter running `poetry update`, you should be able to use the IBM Cloud\nData Engine offline store.\n\n## Define data source\n\nYou can modify the `src/feature_repo/example_repo.py` file to use the new data\nsource. Below is the minimal example of the file:\n\n```python\nfrom ibm_data_engine import DataEngineDataSource\ndriver_stats_source = DataEngineDataSource(\n    name="driver_hourly_stats_source",\n    table="driver_stats_demo",\n    timestamp_field="event_timestamp",\n)\n```\n\n## Define offline store\n\nThen, `feature_repo/feature_store.yaml` must configure the offline store.\n\n```yaml\nproject: test_plugin\nentity_key_serialization_version: 2\nregistry: data/registry.db\nprovider: local\nonline_store:\n    type: redis\n    connection_string: ${REDIS_HOST}:${REDIS_PORT},username=${REDIS_USERNAME},password=${REDIS_PASSWORD},ssl=true,ssl_ca_certs=${REDIS_CERT_PATH},db=0\n\noffline_store:\n    type: ibm_data_engine.DataEngineOfflineStore\n    api_key: ${DATA_ENGINE_API_KEY}\n    instance_crn: ${DATA_ENGINE_INSTANCE_CRN}\n    target_cos_url: ${IBM_CLOUD_OBJECT_STORE_URL}\n```\n\nNotice that you must define the environment variables:\n * `IBM_CLOUD_OBJECT_STORE_URL`\n * `REDIS_HOST`\n * `REDIS_PORT`\n * `REDIS_PASSWORD`\n * `REDIS_CERT_PATH`\n * `DATA_ENGINE_API_KEY`\n * `DATA_ENGINE_INSTANCE_CRN`\n\n## Apply\n\nTo apply the definitions to the registry, run:\n\n```\npoetry run feast -c ./feature_repo apply\n```\n\n## Training\n\nRun training by retrieving historical feature information from feature store\n```\npoetry run python training.py\n```\n## Materialize\n\nTo materialize to Redis, run:\n\n```\npoetry run feast -c ./ materialize \'<START_TIMESTAMP>\'  \'<END_TIMESTAMP>\'\n```\n## Inference\n\n```\npoetry run python inference.py\n```\n',
    'author': 'Michal Siedlaczek',
    'author_email': 'michal.siedlaczek@ibm.com',
    'maintainer': 'Michal Siedlaczek',
    'maintainer_email': 'michal.siedlaczek@ibm.com',
    'url': 'https://github.com/IBM/feast-ibm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
